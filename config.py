import os

from dotenv import load_dotenv

load_dotenv()

WATSONX_SPACE_ID = os.getenv("WATSONX_SPACE_ID", None)
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", None)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY", None)
WATSONX_URL = os.getenv("WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", None)
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
