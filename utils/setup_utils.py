# Utility helpers for the LangGraph notebook

import os
import dotenv

# Tracing imports are optional and only used when init_tracer is called
from opentelemetry import trace
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

dotenv.load_dotenv(dotenv.find_dotenv(), override=True)

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
PHOENIX_PROJECT_NAME = os.environ.get("PHOENIX_PROJECT_NAME")
TAVILY_BASE_URL = os.environ.get("TAVILY_BASE_URL")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")


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

