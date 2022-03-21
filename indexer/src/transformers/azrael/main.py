import base64
import logging
from typing import List

from db import DB
from transform.covalent import Covalent

_LENT_FIELDS  = ["nftAddress", "tokenId", "lentAmount", "lendingId", "lendersAddress",
        "maxRentDuration", "dailyRentPrice", "nftPrice", "isERC721", "paymentToken"]

_RENTED_FIELDS = ["lendingId", "renterAddress", "rentDuration", "rentedAt"]

_RETURNED_FIELDS = ["lendingId", "returnedAt"]

_LENDING_STOPPED_FIELDS =  ["lendingId", "stoppedAt"]

_COLLATERAL_CLAIMED_FIELDS = ["lendingId", "claimedAt"]

Event = lambda name, txn_hash, fields, values: dict(zip(['event', '_id', *fields], [name, txn_hash, *values]))


# todo: needs to inherit an interface that implements flush
# todo: every instance should also take the address it transforms
# todo: as a constructor argument
class Transformer:
    """ReNFT Azrael v1 Transformer"""

    def __init__(self, address: str):

        self._address = address

        self._transformed = []

        self._db_name = "ethereum-indexer"
        self._collection_name = f"{address}-state"
        self._events_of_interest = ["Rented", "Lent", "CollateralClaimed", "LendingStopped", "Returned"]

        self._flush_state = False

        self._db = DB()

    # todo: type that returns transformed transaction
    def entrypoint(self, txn) -> None:
        """_summary_

        Args:
            txn (_type_): _description_
        """

        # 1. check if there is state in the db
        # 2. if there is state in the db, update memory with it
        self.update_memory_state()

        # routes and performs any additional logic
        logging.info(f'Handling transaction at: {txn["block_height"]} block')

        log_events = txn["log_events"]
        # * ensures that events are supplied in the correct order
        log_events = sorted(log_events, key=lambda x: x["log_offset"])

        for event in log_events:

            # * means the event was emitted by a contract that is
            # * not of interest
            if event["sender_address"] != self._address.lower():
                continue

            # todo: this is not good.
            # todo: if this were to happen in an event that pertains to
            # todo: our address, it would corrupt the state
            if event["decoded"] is None:
                logging.warning(f"No name for event: {event}")
                continue

            # events: Rented, Lent, CollateralClaimed, LendingStopped, Returned
            if event["decoded"]["name"] in self._events_of_interest:
                decoded_params = Covalent.decode(event)
                # unique identifier
                tx_hash = f"{event['tx_hash']}_{event['log_offset']}"

                if event["decoded"]["name"] == "Rented":
                    self._on_rented(decoded_params, tx_hash)
                elif event["decoded"]["name"] == "Lent":
                    self._on_lent(decoded_params, tx_hash)
                elif event["decoded"]["name"] == "Returned":
                    self._on_returned(decoded_params, tx_hash)
                elif event["decoded"]["name"] == "LendingStopped":
                    self._on_lending_stopped(decoded_params, tx_hash)
                elif event["decoded"]["name"] == "CollateralClaimed":
                    self._on_collateral_claim(decoded_params, tx_hash)
                
            logging.info(event)

        self._flush_state = True

    # todo: should be part of the interface
    # todo: acts as the means to sync with db state
    def update_memory_state(self) -> None:
        """_summary_"""

        if len(self._transformed) > 0:
            return

        state = self._db.get_all_items(self._db_name, self._collection_name)

        if state is None:
            return

        self._transformed = state

    # todo: should be part of the interface
    def flush(self) -> None:
        """_summary_"""

        if self._flush_state:
            # * write to the db
            self._db.put_items(self._transformed, self._db_name, self._collection_name)
            self._flush_state = False

    def _on_collateral_claim(self, decoded_params, tx_hash: str) -> None:
        # CollateralClaimed(indexed uint256 lendingId, uint32 claimedAt)

        self._transformed.append(Event('CollateralClaimed', tx_hash, _COLLATERAL_CLAIMED_FIELDS, decoded_params))

    def _on_lending_stopped(self, decoded_params, tx_hash: str) -> None:
        # LendingStopped(indexed uint256 lendingId, uint32 stoppedAt)

        self._transformed.append(Event('LendingStopped', tx_hash, _LENDING_STOPPED_FIELDS, decoded_params))

    def _on_returned(self, decoded_params, tx_hash: str) -> None:
        # Returned(indexed uint256 lendingId, uint32 returnedAt)

        self._transformed.append(Event('Returned',tx_hash,  _RETURNED_FIELDS, decoded_params))

    def _on_rented(self, decoded_params, tx_hash: str) -> None:
        # Rented(uint256 lendingId, indexed address renterAddress, uint8 rentDuration, uint32 rentedAt)

        self._transformed.append(Event('Rented', tx_hash, _RENTED_FIELDS, decoded_params))

    def _on_lent(self, decoded_params, tx_hash: str) -> None:
        # Lent(indexed address nftAddress, indexed uint256 tokenId, uint8 lentAmount, uint256 lendingId,
        # indexed address lenderAddress, uint8 maxRentDuration, bytes4 dailyRentPrice,
        # bytes4 nftPrice, bool isERC721, uint8 paymentToken)

        event = Event('Lent', tx_hash, _LENT_FIELDS, decoded_params)
        event['dailyRentPrice'] = unpack_price(event['dailyRentPrice'])
        event['nftPrice'] = unpack_price(event['nftPrice'])

        self._transformed.append(event)


def hex_to_int(s):
    return int(s, 16)

def bytes_to_int(x):
    return int.from_bytes(x, byteorder='big', signed=False)

# TODO: move this to a seperate pypy package
def unpack_price(s):
    # Covalent returns bytes4 types encoded in base64
    s = base64.b64decode(s).hex().upper() # decode into hex
    whole_hex = s[:4]
    decimal_hex = s[4:]

    whole = hex_to_int(whole_hex)
    decimal = hex_to_int(decimal_hex)
    
    # shift right, round to 4 decimal places 
    decimal = round(decimal * 10**-4 , 4)
    return whole + decimal

# todo: do not save empty lists
# todo: block height state is incorrect
