from dotenv import load_dotenv
import os

load_dotenv()  # REQUIRED

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")

# pydantic-ai expects provider:model
MODEL_NAME = "openai:gpt-4o-mini"

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not found in environment")

if not OPENAI_BASE_URL:
    raise RuntimeError("OPENAI_BASE_URL not found in environment")
