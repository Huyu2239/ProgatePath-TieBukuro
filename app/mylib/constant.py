import os

from dotenv import load_dotenv

load_dotenv()


EXTENTIONS = [
    # extentions here
    "cogs.room_manager",
]
PREFIX = os.environ["PREFIX"]
TOKEN = os.environ["TOKEN"]
AUTO_CREATE_CHANNEL_ID = int(os.environ["AUTO_CREATE_CHANNEL_ID"])
