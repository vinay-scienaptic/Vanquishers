__author__ = 'Seetharama'
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from decorators.decorator import CustomLogger, customized_logging

router = APIRouter(
tags = ['Health Check']
)

@router.get('/tick')
def health_check( request: Request):
    @customized_logging(request)
    def main(request):
        # logger = CustomLogger(request)
        # logger.info("Checking the health")
        return JSONResponse(content={"tick":"tock", "status": "I am alive still :)"}, headers={})
    return main(request)

@router.post('/divide')
def health_check( data:dict,request: Request):
    @customized_logging(request)
    def main(request,data):
        logger = CustomLogger(request)
        divide = {}
        divide["divide"] = data["a"]/data["b"]
        logger.info(divide)
        return JSONResponse(content=divide, headers={})
    return main(request,data)
