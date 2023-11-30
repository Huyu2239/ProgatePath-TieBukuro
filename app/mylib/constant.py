import os

from dotenv import load_dotenv

load_dotenv()


DB_URL = os.environ["DB_URL"]
EXTENTIONS = [
    # extentions here
    "cogs.room_manager",
    "cogs.count_time"
]
PREFIX = os.environ["PREFIX"]
TOKEN = os.environ["TOKEN"]
AUTO_CREATE_CHANNEL_ID = int(os.environ["AUTO_CREATE_CHANNEL_ID"])
