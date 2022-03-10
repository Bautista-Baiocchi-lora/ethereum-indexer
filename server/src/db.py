import os
from typing import Any

import motor.motor_asyncio
from dotenv import load_dotenv

from interfaces.idb import IDB

load_dotenv()

MONGO_URI = f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASSWORD']}@{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}"

class DB(IDB):

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

    async def get_item(self, identifier: str, database_name: str, collection_name: str) -> Any:
        collection = self.client[database_name][collection_name]

        result  = await collection.find_one({"_id": identifier})
        return result
