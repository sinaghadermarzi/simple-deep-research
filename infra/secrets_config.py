# secrets_config.py
import os
import dotenv

dotenv.load_dotenv()

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY", "")
TAVILY_API_KEY  = os.getenv("TAVILY_API_KEY", "")


assert OPENAI_API_KEY, "OPENAI_API_KEY is required"
assert TAVILY_API_KEY, "TAVILY_API_KEY is required"
