__author__ = 'Seetharama'

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from decorators.decorator import customized_logging

#importing the code from other files
from routers.application_finder.rollup import rollup as application_finder_rollup


router = APIRouter(
tags = ['Internal']
)

@router.post('/find')
def rollup_func(data:dict,request: Request):
    @customized_logging(request)
    def main(data,request):
        resp = application_finder_rollup.main_fuct(data,request)
        return JSONResponse(content=resp)
    return main(data,request)

@router.get('/find')
def rollup_func(request: Request):
    @customized_logging(request)
    def main():
        resp = { "Sample Request": { "request_body": { "OrgID":"", "CollectionName": "flow_1234", "_ApplicationIDs": [ 1234 ], "_UniqueField": "sources.values.input.id", "_limit": 10, "_Count":True, "_Projection":True, "_find": { "sources.values.input.id": 1234 }, "_Date": { "From": "2022-05-26T00:00:00.001Z", "To": "2022-05-31T00:00:00.001Z" } }, "Details": "Remove the underscore (_) to make use of that option" }, "Help": { "Details": "This is a simple API service to fetch the Record from Mongo Collection", "Required": { "OrgID":{ "Details": "ID of the Organization", "Example": "085ffggb-ppb8-4998-2c35-pc35sa38hjkl" }, "CollectionName": { "Details": "Name of the Collection", "Example": "flow_12345", "Note": "If only CollectionName is sent, latest record from the collection would be returned" } }, "Options": { "Find/find": { "Details": "Provide the find query to be executed on the mongo", "Example": { "1": { "app_id": 123 }, "2": { "app_id": { "$exists":True } } } }, "Projection/projection": { "Options": "true/false", "Details": "If this is set as true, then if you query for find, you will get the projected data in the query", "Note": { "1": "Find query should be provided", "2": "When Projection is enabled, limit has no effect in the querying" } }, "Count/count": { "Options": "true/false", "Details": "If this is set as true, then if you query for ApplicationIDs/Date range, you will get the number of records for that ApplicationIDs/Date range", "Note": { "1": "Count has most precedence", "2": "When count is enabled, limit has no effect in the querying" } }, "Date/date": { "Required": { "From": { "Details": "From which date the export to be taken", "Example": "2022-05-26T00:00:00.001Z or 2022-05-26 00:00:00 or 2022-05-26" }, "To": { "Details": "To which date the export to be taken", "Example": "2022-05-26T00:00:00.001Z or 2022-05-26 00:00:00 or 2022-05-26" } }, "Details": "To export the records for a certain time range", "Note": { "1": "Date has second most precedence", "2": "When Date field is passed, passing application id has no effect in the querying" } }, "ApplicationIDs": { "Details": "Application ID/Unique ID for which to be queried as a list/array", "Note": "Will also require UniqueField to be passed in the request", "Example": "[123,234,567]" }, "UniqueField": { "Details": "to Query the Application ID/Unique ID, will have to provide the path for the Application ID/Unique ID to find", "Note": "Will also require ApplicationIDs to be passed in the request", "Example": "sources.values.input.Application.applicationID" }, "Limit/limit": { "Default": 1, "Details": "To limit the number of records to be fetched", "Note": { "Summary": "If ApplicationIDs is passed in the request, and also sent a limit, we will get those many records from the collection for that application id ", "Explanation": "If Application id [12,13] and limit of 3 was sent in the request, assume in the collection for application id 12 there are 10 records, in the response we will get 3 records for that application id since limit was 3" }, "Other Use cases": { "1": "if only limit passed with CollectionName and no ApplicationIDs and UniqueField is sent, then this will return latest record according to the limit set, if 10 was the limit, this will return 10 latest record from the collection" } } } } }
        return JSONResponse(content=resp)
    return main()
