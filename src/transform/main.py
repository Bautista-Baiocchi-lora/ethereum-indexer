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

        # * to read the raw transactions from the database
        self._db = DB()

    def transform(self) -> None:
        ...

    def flush(self) -> None:
        ...
