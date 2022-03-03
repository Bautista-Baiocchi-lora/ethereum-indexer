from typing import Any
import logging

from transform.covalent import Covalent

# todo: needs to inherit some interface?
class Transformer:
    def __init__(self, address: str):

        self._address = address

        # todo: remove. purely to test
        # let's have address -> kong id
        self.transformed = {}

    # todo: type that returns transformed transaction
    def entrypoint(self, txn) -> Any:
        # routes and performs any additional logic
        logging.info(f'Handling transaction at: {txn["block_height"]} block')

        log_events = txn["log_events"]
        # * ensures that events are supplied in the correct order
        log_events = sorted(log_events, key=lambda x: x["log_offset"])

        for event in log_events:

            # * means the event was emitted by something that is
            # * not supported
            if event["sender_address"] != self._address.lower():
                continue

            # todo: this is not good.
            if event["decoded"] is None:
                logging.warn(f"No name for event: {event}")
                continue

            # todo: you can also have a decoded like this:
            # 'decoded': {'name': 'Transfer', 'signature': 'Transfer(indexed address from, indexed address to, uint256 value)', 'params': None}}
            # which happens on block height 13353454
            # this means that we should have mechanism that pulls the raw
            # transaction off a node

            if event["decoded"]["name"] == "Transfer":
                decoded_params = Covalent.decode(event)
                self._on_transfer(*decoded_params)

            logging.info(event)

        # todo
        return []

    def _on_transfer(self, from_, to_, value_) -> None:
        # Transfer(indexed address from, indexed address to, uint256 value)

        # todo: make this a constant somewhere
        if from_ != "0x0000000000000000000000000000000000000000":
            prev = self.transformed[from_]
            prev.remove(value_)
            self.transformed[from_] = prev

        if to_ in self.transformed:
            self.transformed[to_].append(value_)
        else:
            self.transformed[to_] = [value_]
