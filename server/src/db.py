import os
from typing import Any, Dict, List, Optional

import motor.motor_asyncio
from dotenv import load_dotenv

from interfaces.idb import IDB

load_dotenv()

MONGO_URI = f"mongodb://{os.environ['MONGO_USER']}:{os.environ['MONGO_PASSWORD']}@{os.environ['MONGO_HOST']}:{os.environ['MONGO_PORT']}"

class DB(IDB):

    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

    def _get_collection(self, database_name: str, collection_name: str):
        return self.client[database_name][collection_name]

    async def get_item(self, identifier: str, database_name: str, collection_name: str) -> Any:
        collection = self._get_collection(database_name, collection_name)

        result  = await collection.find_one({"_id": identifier})
        return result

    async def get_N_items(self, database_name: str, collection_name: str, N: int, options: Optional[Dict] = None) -> List[Any]:
        cursor = self._get_collection(database_name, collection_name).find()

        if options is not None:
            
            if "sort" in options:
                # [('fieldName1', pymongo.ASCENDING), ('fieldName2', pymongo.DESCENDING)]
                cursor.sort(options["sort"])

            cursor.allow_disk_use(True)

            return await cursor.to_list(length=N)

        return await cursor.to_list(length=N)
