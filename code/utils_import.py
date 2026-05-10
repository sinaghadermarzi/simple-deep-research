# Utility helpers for the LangGraph notebook

import os
import constants

# Tracing imports are optional and only used when init_tracer is called
from opentelemetry import trace
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor


# Load local environment file used by the workshop
# Keep the same relative path as the notebook used

OPENAI_BASE_URL = constants.OPENAI_BASE_URL
OPENAI_API_KEY = constants.OPENAI_API_KEY
OPENAI_MODEL = constants.OPENAI_MODEL
PHOENIX_PROJECT_NAME = constants.PHOENIX_PROJECT_NAME
TAVILY_BASE_URL = constants.TAVILY_BASE_URL
TAVILY_API_KEY = constants.TAVILY_API_KEY


# configure the Phoenix tracer
if os.environ.get("PHOENIX_COLLECTOR_ENDPOINT"):
    tracer_provider = register(
        project_name=PHOENIX_PROJECT_NAME, 
        auto_instrument=False 
    )
    
else:
    tracer_provider = trace.NoOpTracerProvider()

LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
tracer = trace.get_tracer(__name__)

