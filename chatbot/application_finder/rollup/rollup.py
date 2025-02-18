__author__ = 'Seetharama'

from decorators.decorator import CustomLogger
import os
import json
import pymongo
import dateutil.parser as parser
from bson import json_util
from bson.objectid import ObjectId

class ApplicationExport():
    def __init__(self,data):
        self.data =  data

    def main(self):

        uri = os.environ.get("config__mongo_connection_string")
        db = "database_" + self.data['OrgID']
        resp=[]
        try:
            col_name = self.data['CollectionName']
        except KeyError:
            return {"Error":"Please provide the Collection Name"}

        count = self.data['Count'] if 'Count' in self.data else self.data['count'] if 'count' in self.data else False
        uniqueids = self.data['ApplicationIDs'] if "ApplicationIDs" in self.data else []
        limit = self.data['limit'] if "limit" in self.data else self.data['Limit'] if "Limit" in self.data else 1
        limit_flag = True if "limit" in self.data else True if "Limit" in self.data else False
        date_to_export = self.data['Date'] if "Date" in self.data else ""
        find = self.data["find"] if "find" in self.data else self.data["Find"] if "Find" in self.data else None
        projection = self.data["projection"] if "projection" in self.data else self.data["Projection"] if "Projection" in self.data else False
        try:
            query = self.data['UniqueField']
        except KeyError:
            if uniqueids != []:
                return {"Error":"Please provide the UniqueField to query"}
            else:
                query = {}

        if date_to_export != "" and count == False:
            try:
                resp = (ApplicationExport.mongo_query_with_date(col_name,date_to_export,uri,db))
                element_list = [ ApplicationExport.parse_json(element) for element in resp]
                return element_list
            except:
                return {"Error":"Please provide a valid datetime range"}
        elif date_to_export != "" and count == True:
            try:
                return {"Count":ApplicationExport.mongo_query_date_count(col_name,date_to_export,uri,db)}
            except:
                return {"Error":"Please provide a valid datetime range"}

        if uniqueids != []:
            if count:
                for uniqueid in uniqueids:
                    resp.append({uniqueid: ApplicationExport.mongo_query_count(uniqueid,col_name,query,uri,db)})
                return resp
            for uniqueid in uniqueids:
                resp.append(ApplicationExport.mongo_query(uniqueid,col_name,query,limit,uri,db))
                element_list = [ ApplicationExport.parse_json(element) for element in resp]
        else:
            if find:
                if projection and count:
                    resp.append(ApplicationExport.mongo_query_projection_count(col_name,find,uri,db))
                elif count:
                    resp.append(ApplicationExport.mongo_query_find_count(col_name,find,uri,db))
                elif projection:
                    resp.append(ApplicationExport.mongo_query_projection(col_name,find,uri,db))
                else:
                    resp.append(ApplicationExport.mongo_query_find(col_name,find,uri,db,limit,limit_flag))
                element_list = [ ApplicationExport.parse_json(element) for element in resp]
                return element_list
            if count:
                return ApplicationExport.mongo_query_count(None,col_name,None,uri,db)
            resp = ApplicationExport.mongo_query(None,col_name,None,limit,uri,db)
            element_list = [ ApplicationExport.parse_json(element) for element in resp]
        return element_list

    @staticmethod
    def mongo_query(uniqueid,col_name,query,limit,uri,db_name):
        client = pymongo.MongoClient(uri)
        db = client[db_name]
        col = db[col_name]
        if query == None:
            data = list(col.find().sort("createdAt", -1).limit(limit))
        elif query == "_id":
            data = list(col.find({"_id":ObjectId(uniqueid)}))
        else:
            data = list(col.find({query:uniqueid}).sort("createdAt", -1).limit(limit))
        if data != []:
            #for each_data in data:
            resp = data
        else:
            resp = {'App id': uniqueid, 'status':'data not found'}
        return resp

    @staticmethod
    def mongo_query_with_date(col_name,date_to_export,uri,db_name):
        client = pymongo.MongoClient(uri)
        db = client[db_name]
        col = db[col_name]
        try:
            date_time_from = parser.parse(date_to_export["From"])
            date_time_to = parser.parse(date_to_export["To"])
        except KeyError:
            return {"Error":"Please provide a valid datetime range"}
        data = list(col.find({"createdAt":{"$gte":date_time_from, "$lte": date_time_to}}).sort("createdAt", -1))
        if data != []:
            resp = data
        else:
            resp = {'status':'data not found for that time period'}
        return resp

    @staticmethod
    def mongo_query_date_count(col_name,date_to_export,uri,db_name):
        client = pymongo.MongoClient(uri)
        db = client[db_name]
        col = db[col_name]
        try:
            date_time_from = parser.parse(date_to_export["From"])
            date_time_to = parser.parse(date_to_export["To"])
        except:
            return {"Error":"Please provide a valid datetime range"}
        return col.count_documents({"createdAt":{"$gte":date_time_from, "$lte": date_time_to}})

    @staticmethod
    def mongo_query_count(uniqueid,col_name,query,uri,db_name):
        client = pymongo.MongoClient(uri)
        db = client[db_name]
        col = db[col_name]
        if query == None:
            data = col.count_documents({})
        elif query == "_id":
            data = col.count_documents({"_id":ObjectId(uniqueid)})
        else:
            data = col.count_documents({query:uniqueid})
        return data

    @staticmethod
    def mongo_query_find(col_name,query,uri,db_name,limit,limit_flag):
        client = pymongo.MongoClient(uri)
        db = client[db_name]
        col = db[col_name]
        if limit_flag:
            data = list(col.find(query).limit(limit))
        else:
            data = list(col.find(query))
        return data

    @staticmethod
    def mongo_query_find_count(col_name,query,uri,db_name):
        client = pymongo.MongoClient(uri)
        db = client[db_name]
        col = db[col_name]
        data = col.count_documents(query)
        return data

    @staticmethod
    def mongo_query_projection(col_name,query,uri,db_name):
        client = pymongo.MongoClient(uri)
        db = client[db_name]
        col = db[col_name]
        try:
            data = list(col.find({},query))
        except pymongo.errors.OperationFailure as e:
            data = {"error": str(e)}
        return data

    @staticmethod
    def mongo_query_projection_count(col_name,query,uri,db_name):
        client = pymongo.MongoClient(uri)
        db = client[db_name]
        col = db[col_name]
        try:
            data = len(list(col.find({},query)))
        except pymongo.errors.OperationFailure as e:
            data = {"error": str(e)}
        return data

    @staticmethod
    def parse_json(data):
        return json.loads(json_util.dumps(data))


def main_fuct(data,request):
    logger = CustomLogger(request)
    try:
        obj = ApplicationExport(data)
        resp = obj.main()
        logger.info("Found the Application")
    except:
        logger.info("Errored while finding Application")
        resp = {"Error":"Failed to fetch the application"}
    return resp
