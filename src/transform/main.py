import logging
import json
import os

from interfaces.itransform import ITransform
from db import DB


class Transform(ITransform):
    def __init__(self, to_transform: str):
        self._to_transform = to_transform

        # ! transformers should always have a config.json inside
        # ! that describes the address to transform, as well as,
        # ! supported events
        config_path = os.path.join(
            os.path.abspath(os.path.dirname(os.path.dirname(__file__))),
            "transformers",
            self._to_transform,
            "config.json",
        )

        # * 1. information about what address to transform
        # * 2. information about events are handled
        self._config = json.loads(open(config_path).read())

        # todo: validate that the address in config is valid
        # todo: validate that the address is being scraped (i.e. is in the db)
        # todo: validate that the name of the events is lower cased event name
        # from the scraped transactions

        # block number up to which the extraction has happened
        self._block_height: int = 0

        # todo: type of state
        self._state = []

        self._db_name = "ethereum-indexer"

        # * to read the raw transactions from the database
        self._db = DB()

    def __setattr__(self, key, value):
        # https://towardsdatascience.com/how-to-create-read-only-and-deletion-proof-attributes-in-your-python-classes-b34cd1019c2d

        forbid_reset_on = ["_to_transform", "_config", "_db_name", "_db"]
        for k in forbid_reset_on:
            if key == k and hasattr(self, k):
                raise AttributeError(
                    "The value of the address attribute has already been set, and can not be re-set."
                )

        self.__dict__[key] = value

    def _get_state_collection_name(self) -> str:
        # todo: will be more than one address later
        return f"{self._get_address_from_config()}-state"

    def _get_address_from_config(self) -> str:
        return self._config["address"][0]

    def _get_block_height_collection_name(self) -> str:
        return f"{self._get_address_from_config()}-block-height-state"

    def _determine_block_height(self) -> None:
        """
        This ensures we do not extract all the data all the time, but only
        the new stuff. This is also helpful in case the binary raises and
        we need to restart it.
        """

        block_height_item = self._db.get_any_item(
            self._db_name, self._get_block_height_collection_name(self._address)
        )
        # If it is None, then we have already set it to 0 in the __init__
        if block_height_item is None:
            return

        self._block_height = block_height_item["block_height"]

    def _update_block_height(self, new_block_height: int, for_address: str) -> None:
        """
        Args:
            new_block_height (int): _description_
            for_address (str): _description_
        """

        collection_name = self._get_block_height_collection_name(for_address)
        # _id: 1, because we are only ever storing single block_height value per address
        item = {"_id": 1, "block_height": new_block_height}
        self._db.put_item(item, self._db_name, collection_name)

    # todo: return type
    def _read_raw_transactions_after_block(self):
        """
        Pulls all transactions after block height, and sorts them in ascending order
        """

        raw_transactions = self._db.get_all_items(
            self._db_name,
            self._get_address_from_config(),
            {
                "query_clause": {"block_height": {"$gt": self._block_height}},
                "sort": {"sort_by": "block_height", "direction": 1},
            },
        )

        return raw_transactions

    def transform(self) -> None:
        # 1. Retrieve the last block up to which we have transformed the txns
        # 2. Read the raw transactions after that block
        # 3. Pass in the right order these transactions into individual handlers
        # 4. Handlers return transformed data which we store here in memory
        # 5. Determine the last block from these txns
        # 6. Update the last block

        # 1.
        self._determine_block_height()

        # 2.
        raw_transactions = self._read_raw_transactions_after_block()

        # 3.
        for txn in raw_transactions:
            ...

    def flush(self) -> None:

        if len(self._state) == 0:
            return

        self._db.put_items(self._state, self._db_name, self._collection_name)

        self._state = []
