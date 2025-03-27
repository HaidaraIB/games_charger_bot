import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    SATOFILL_TOKEN = os.getenv("SATOFILL_TOKEN")
    SESSION = os.getenv("SESSION")
    OWNER_ID = int(os.getenv("OWNER_ID"))
    ERRORS_CHANNEL = int(os.getenv("ERRORS_CHANNEL"))
    PHOTOS_ARCHIVE = int(os.getenv("PHOTOS_ARCHIVE"))
    FORCE_JOIN_CHANNEL_ID = int(os.getenv("FORCE_JOIN_CHANNEL_ID"))
    FORCE_JOIN_CHANNEL_LINK = os.getenv("FORCE_JOIN_CHANNEL_LINK")
    DB_PATH = os.getenv("DB_PATH")
