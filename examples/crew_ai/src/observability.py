import os

from openinference.instrumentation.crewai import CrewAIInstrumentor
from openinference.instrumentation.langchain import LangChainInstrumentor
from openinference.instrumentation.litellm import LiteLLMInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_observability():
    headers = {
        "Galileo-API-Key": os.environ.get("GALILEO_API_KEY", "your_galileo_api_key_here"),
        "project": os.environ.get("GALILEO_PROJECT", "crew"),  # or "project":"example",
        "logstream": os.environ.get("GALILEO_LOGSTREAM", "default"),
    }
    os.environ["OTEL_EXPORTER_OTLP_TRACES_HEADERS"] = ",".join([f"{k}={v}" for k, v in headers.items()])

    endpoint = "https://app.galileo.ai/api/galileo/otel/traces"

    # Setup tracer provider
    tracer_provider = trace_sdk.TracerProvider()
    tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint)))
    LiteLLMInstrumentor().instrument(tracer_provider=tracer_provider)
    CrewAIInstrumentor().instrument(tracer_provider=tracer_provider)
    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
