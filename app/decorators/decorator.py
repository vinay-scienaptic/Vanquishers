import traceback
from fastapi.responses import JSONResponse
from functools import wraps
from errors import (
    ServerError,
    BadRequestError,
    RequestKeyError,
    RequestValueError,
)
import ipaddress
import loggers
from opentelemetry import trace
from tracers import provider as trace_provider
# from metrics import provider as metrics_provider
from opentelemetry.trace import Status, StatusCode
# from opentelemetry import metrics
from fastapi import Request
import json
import time

class CustomLogger:
    def __init__(self, request):
        if isinstance(request, Request):
            self.request = request
            self.host = self.request.headers.get("host")
        else:
            self.host = request
        if (
            (self.host not in ["", None])
            and self.host[0:9] != "localhost"
            and not self.is_ipv4((self.host.split(":"))[0])
        ):
            if isinstance(request, Request):
                self.host = self.request.headers.get("host")
            else:
                self.host = request
        else:
            self.host = "No Host Header defined"
        self.time_taken = time.time()
        self.tracer = trace.get_tracer(__name__, tracer_provider=trace_provider)
        # self.meter = metrics.get_meter(__name__, meter_provider=metrics_provider)

    def is_ipv4(self, string):
        try:
            ipaddress.IPv4Network(string)
            return True
        except ValueError:
            return False

    def record_request(self):
        with self.tracer.start_as_current_span("record_request") as span:
            span = CustomTracer(self.request).set_attributes(span)
            # self.meter.create_counter("record_request").add(1)
            if self.host != "No Host Header defined":
                loggers.logger.info(
                    f'[{self.host}] : Content-Type:{self.request.headers.get("content-type")}'
                )

    def record_response(self, response):
        with self.tracer.start_as_current_span("record_response") as span:
            span = CustomTracer(self.request).set_attributes(span)
            # self.meter.create_counter("record_response").add(1)
            if self.host != "No Host Header defined":
                if response.status_code in [200,"200"]:
                    loggers.logger.info(
                        f'[{self.host}] : Status-Code:{response.status_code} - Content-Length:{response.headers.get("content-length")} - Content-Type:{response.headers.get("content-type")} - Response-Time:{time.time() - self.time_taken:.2f} secs'
                    )
                    span.set_status(Status(StatusCode.OK))
                else:
                    loggers.logger.error(
                        f'[{self.host}] : Status-Code:{response.status_code} - Content-Length:{response.headers.get("content-length")} - Content-Type:{response.headers.get("content-type")} - Status: {json.loads(response.body.decode("utf-8"))["status"]} - Content:{json.loads(response.body.decode("utf-8"))["message"]} - Response-Time:{time.time() - self.time_taken:.2f} secs'
                    )
                    span.set_status(Status(StatusCode.ERROR))
            # self.meter.create_counter(
            #     "status_code_" + str(response.status_code)
            #     if response.status_code
            #     else "500"
            # ).add(1)

    def info(self, msg):
        loggers.logger.info(f"[{self.host}] : {msg}")

    def warning(self, msg):
        loggers.logger.warning(f"[{self.host}] : {msg}")

    def error(self, msg):
        loggers.logger.error(f"[{self.host}] : {msg}")


class CustomTracer:
    def __init__(self, request):
        if isinstance(request, Request):
            self.request = request
            self.host = self.request.headers.get("host")
        else:
            self.host = request
        if (
            (self.host not in ["", None])
            and self.host[0:9] != "localhost"
            and not self.is_ipv4((self.host.split(":"))[0])
        ):
            if isinstance(request, Request):
                self.host = self.request.headers.get("host")
            else:
                self.host = request
        elif self.is_ipv4((self.host.split(":"))[0]):
            self.host = "internal"
        else:
            self.host = "No Host Header defined"

    def is_ipv4(self, string):
        try:
            ipaddress.IPv4Network(string)
            return True
        except ValueError:
            return False

    def set_attributes(self, span):
        span.set_attribute("host", self.host)
        if isinstance(self.request, Request):
            span.set_attribute(
                "content-type",
                (
                    self.request.headers.get("content-type")
                    if self.request.headers.get("content-type")
                    else "txt/plain"
                ),
            )
            span.set_attribute(
                "content-length",
                (
                    self.request.headers.get("content-length")
                    if self.request.headers.get("content-length")
                    else 0
                ),
            )
        return span


def customized_logging(request):
    def logging_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__, tracer_provider=trace_provider)
            # meter = metrics.get_meter(__name__, meter_provider=metrics_provider)
            with tracer.start_as_current_span("call_" + func.__name__) as span:
                span = CustomTracer(request).set_attributes(span)
                logger = CustomLogger(request)
                span.set_status(Status(StatusCode.OK))
                # meter.create_gauge("call_" + func.__name__).set(1)
                logger.record_request()
                try:
                    response = func(*args, **kwargs)
                    logger.record_response(response)
                except TypeError as te:
                    logger.error(traceback.format_exc())
                    response = JSONResponse(
                        content=BadRequestError(
                            traceback.format_exception_only(te.__class__, te)
                        ).to_dict(),
                        status_code=400,
                    )
                    logger.record_response(response)
                    return response
                except KeyError as ke:
                    logger.error((traceback.format_exc()))
                    response = JSONResponse(
                        content=RequestKeyError(
                            traceback.format_exception_only(ke.__class__, ke)
                        ).to_dict(),
                        status_code=500,
                    )
                    logger.record_response(response)
                    return response
                except ValueError as ve:
                    logger.error((traceback.format_exc()))
                    response = JSONResponse(
                        content=RequestValueError(
                            traceback.format_exception_only(ve.__class__, ve)
                        ).to_dict(),
                        status_code=500,
                    )
                    logger.record_response(response)
                    return response
                except Exception as e:
                    logger.error(traceback.format_exc())
                    response = JSONResponse(
                        content=ServerError(
                            traceback.format_exception_only(e.__class__, e)
                        ).to_dict(),
                        status_code=500,
                    )
                    logger.record_response(response)
                    return response

            return response

        return wrapper

    return logging_decorator
