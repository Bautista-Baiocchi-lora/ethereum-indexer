from typing import Dict, Any
import logging


# todo: needs to inherit some interface?
class Transformer:

    # todo: type that returns transformed transaction
    def entrypoint(self, txn) -> Any:
        # routes and performs any additional logic
        logging.info(f'Handling {txn["block_height"]}')

        return []

    def _on_transfer(self, decoded: Dict) -> None:
        # Transfer(indexed address from, indexed address to, uint256 value)
        ...
