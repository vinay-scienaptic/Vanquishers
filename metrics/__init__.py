import os
from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource

resource = Resource.create(attributes={"service.name": "rollup-service"})

# Set up the meter provider and exporter
metric_exporter = OTLPMetricExporter(endpoint=os.environ.get("OTLP_COLLECTOR_ENDPOINT"))
metric_reader = PeriodicExportingMetricReader(metric_exporter)

# Create a MeterProvider and add the MetricReader
provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)
