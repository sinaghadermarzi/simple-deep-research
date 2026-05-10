import dotenv
import os

dotenv.load_dotenv("../.env", override=True)

OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
PHOENIX_PROJECT_NAME = os.environ.get("PHOENIX_PROJECT_NAME")
TAVILY_BASE_URL = os.environ.get("TAVILY_BASE_URL")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")