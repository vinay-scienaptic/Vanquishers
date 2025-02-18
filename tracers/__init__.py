from opentelemetry import trace

# from opentelemetry.context import get_current
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
import os

# Set up the tracer provider and exporter
resource = Resource.create(attributes={"service.name": "rollup-service"})
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Create an OTLP exporter
otlp_exporter = OTLPSpanExporter(endpoint=os.environ.get("OTLP_COLLECTOR_ENDPOINT"))

# Add the exporter to the tracer provider
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)
