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

        # todo: type of state
        self._state = []

        self._db_name = "ethereum-indexer"
        # todo: will be more than one address later
        self._collection_name = f'{self._config["address"][0]}-state'

        # * to read the raw transactions from the database
        self._db = DB()

    def transform(self) -> None:
        # 1. Retrieve the last block up to which we have transformed the txns
        # 2. Read the raw transactions after that block
        # 3. Pass in the right order these transactions into individual handlers
        # 4. Handlers return transformed data which we store here in memory
        # 5. Determine the last block from these txns
        # 6. Update the last block
        ...

    def flush(self) -> None:

        if len(self._state) == 0:
            return

        self._db.put_items(self._state, self._db_name, self._collection_name)

        self._state = []
