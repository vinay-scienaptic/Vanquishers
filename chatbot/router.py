from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from decorators.decorator import customized_logging

import model as training_model

router = APIRouter(
prefix='/OjhsgoUyLL',
tags = ['LLM Model']
)


@router.post('/llmmodel')
def main_llm_func(request: Request):
    @customized_logging(request)
    def main(request):
        resp = training_model.ask_question(request)
        return JSONResponse(content=resp)
    return main(request)