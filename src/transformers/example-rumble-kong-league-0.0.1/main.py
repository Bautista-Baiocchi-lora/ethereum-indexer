from typing import Dict
from db import DB

# todo: needs to inherit some interface?
class Transformer:
    def __init__(self):
        self._db = DB()

    def on_transfer(decoded: Dict) -> None:
        # Transfer(indexed address from, indexed address to, uint256 value)
        ...
