from typing import List, Dict, Any, Optional
from pymongo import MongoClient

from interfaces.idb import IDB


class DB(IDB):
    def __init__(self):
        self.client = MongoClient(port=27017)

    def put_item(self, item: Dict, table_name: str, collection_name: str) -> None:
        db = self.client[table_name]
        db[collection_name].replace_one({"_id": item["_id"]}, item, upsert=True)

    def get_item(self, id: str, table_name: str, collection_name: str) -> Any:
        db = self.client[table_name]
        return db[collection_name].find({"_id": id})

    # todo: concrete type for options
    def get_all_items(
        self, table_name: str, collection_name: str, options: Optional[Dict]
    ) -> List[Any]:
        db = self.client[table_name]

        if options is None:
            return list(db[collection_name].find())
        else:
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

    def get_any_item(self, table_name: str, collection_name: str) -> Any:
        """
        MongoDB will return an empty list is collection does not exist
        """
        all_items = self.get_all_items(table_name, collection_name)
        if len(all_items) == 0:
            return None
        else:
            return all_items[0]
