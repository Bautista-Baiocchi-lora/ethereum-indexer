from typing import Dict, Any
from db import DB

# todo: needs to inherit some interface?
class Transformer:
    def __init__(self):
        self._db = DB()

    # todo: type that returns transformed transaction
    def entrypoint(self) -> Any:
        # routes and performs any additional logic
        ...

    def _on_transfer(self, decoded: Dict) -> None:
        # Transfer(indexed address from, indexed address to, uint256 value)
        ...
