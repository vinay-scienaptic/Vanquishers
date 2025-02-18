
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from chatbot.health_check import router as health_check
from chatbot.application_finder import router as application_finder

import chatbot

import uvicorn

from tracers import provider as trace_provider
from metrics import provider as metrics_provider
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from decorators.decorator import CustomLogger, customized_logging
from fastapi import Request
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)




app.include_router(chatbot.router,prefix="/rollup",responses={404: {"description": "Not found"}})

FastAPIInstrumentor().instrument_app(
    app, tracer_provider=trace_provider, meter_provider=metrics_provider
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config="log.ini", access_log=False)
