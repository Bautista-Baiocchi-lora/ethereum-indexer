from typing import List, Dict, Any, Optional
from pymongo import MongoClient

from interfaces.idb import IDB


class DB(IDB):
    def __init__(self):
        self.client = MongoClient(port=27017)

    def put_item(self, item: Dict, database_name: str, collection_name: str) -> None:
        db = self.client[database_name]
        db[collection_name].replace_one({"_id": item["_id"]}, item, upsert=True)

    def get_item(
        self, identifier: str, database_name: str, collection_name: str
    ) -> Any:
        db = self.client[database_name]
        return db[collection_name].find({"_id": identifier})

    # todo: concrete type for options
    def get_all_items(
        self, database_name: str, collection_name: str, options: Optional[Dict] = None
    ) -> List[Any]:
        db = self.client[database_name]

        if "sort" in options:
            # todo: validation
            sort_by = options["sort"]["sort_by"]
            direction = options["sort"]["direction"]

            query_clause = {}

            if "query_clause" in options:
                query_clause = options["query_clause"]

            return list(
                db[collection_name]
                .find(query_clause, allow_disk_use=True)
                .sort(sort_by, direction)
            )

        return list(db[collection_name].find())

    def get_any_item(
        self, database_name: str, collection_name: str, _: Optional[Dict] = None
    ) -> Any:
        """
        MongoDB will return an empty list is collection does not exist
        """
        all_items = self.get_all_items(database_name, collection_name)
        if len(all_items) == 0:
            return None
        return all_items[0]
