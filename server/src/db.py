import os

import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASSWORD']}@{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)


