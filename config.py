import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

FREE_REQUESTS_PER_DAY = int(
    os.getenv("FREE_REQUESTS_PER_DAY", "5")
)

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.5"
)
