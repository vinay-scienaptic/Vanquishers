import logging
import os
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource

# Instrument logging
LoggingInstrumentor().instrument(set_logging_format=True)

resource = Resource.create(attributes={"service.name": "rollup-service"})

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create an OTLP log exporter
log_exporter = OTLPLogExporter(endpoint=os.environ.get("OTLP_COLLECTOR_ENDPOINT"))

# Create a logger provider and add a log processor
logger_provider = LoggerProvider(resource=resource)
logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter=log_exporter))

# Set the logger provider
LoggingHandler(logger_provider=logger_provider, level=logging.INFO)
logger.addHandler(LoggingHandler(logger_provider=logger_provider))
