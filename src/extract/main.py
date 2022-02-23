from typing import Dict, List
import logging

from interfaces.iextract import IExtract
from load.main import Load
from utils.misc import remove_duplicates
from db import DB
from extract.covalent import Covalent

# todo: eventually would want each extractor running in its own process
# for now the solution around that would be to simply run this pipeline
# multiple times


class Extract(IExtract):
    def __init__(self, address: List[str]):
        """
        Args:
            address (List[str]): list of addresses for which to extract the raw historical
        transaction data.
        """
        # todo: big issues with eth hash lib. no checksum validation for now
        self._validate_address(address)

        self._address: List[str] = address
        # block number up to which the extraction has happened
        self._block_height: Dict[str, int] = dict(
            zip(self._address, [0 for _ in self._address])
        )

        self._covalent = Covalent()

        self._db_name = "ethereum-indexer"

        self._db = DB()
        self._load = Load()

        # todo: type of transactions
        self._transactions = []

    def __setattr__(self, key, value):
        # https://towardsdatascience.com/how-to-create-read-only-and-deletion-proof-attributes-in-your-python-classes-b34cd1019c2d

        # re-setting the _address, _db_name, _db, _load is not allowed
        forbid_reset_on = ["_address", "_db_name", "_db", "_load"]
        for k in forbid_reset_on:
            if key == k and hasattr(self, k):
                raise AttributeError(
                    "The value of the address attribute has already been set, and can not be re-set."
                )

        self.__dict__[key] = value

    def _validate_address(self, address: List[str]) -> None:
        """_summary_

        Args:
            address (List[str]): _description_

        Raises:
            InvalidAddress: _description_
            ValueError: _description_
        """

        # for a in address:
        #     validate_address(a)

        # * ensures there are no duplicate addresses
        # * note that if multiple instances of the pipeline
        # are running with duplicate addresses, that **will**
        # cause errors
        without_dupes = remove_duplicates(address)

        if len(without_dupes) != len(address):
            raise ValueError("There can't be duplicates in address", address)

    def _get_block_height_collection_name(self, address: str) -> str:
        return f"{address}-block-height"

    def _determine_block_height(self) -> None:
        """
        Goes through each address and determines its `block_height` value.
        This ensures we do not extract all the data all the time, but only
        the new stuff. This is also helpful in case the binary raises and
        we need to restart it.
        """

        for addr in self._address:
            block_height = self._db.get_any_item(
                self._db_name, self._get_block_height_collection_name(addr)
            )
            # If it is None, then we have already set it to 0 in the
            # __init__. This will signal the extractor to extract
            # the complete history of the address
            if block_height is None:
                continue

            self._block_height[addr] = block_height

    def _update_block_height(self, new_block_height: int, for_address: str) -> None:
        """
        After extracting the transactions update the db with the latest block height.

        Args:
            new_block_height (int): _description_
            for_address (str): _description_
        """

        collection_name = self._get_block_height_collection_name(for_address)
        # _id: 1, because we are only ever storing single block_height value per address
        item = {"_id": 1, "block_height": new_block_height}
        self._db.put_item(item, self._db_name, collection_name)

    def _request_transactions(self, for_address: str, page_number: int) -> None:
        response = self._covalent.request_transactions(for_address, page_number)
        return response

    def _extract_txn_history_since(self, block_height: int, for_address: str) -> None:
        """
        Makes requests to Covalent, and only extracts transactions after `block_height`
        block number.

        Args:
            block_height (int): We have data for this address up to and including this
            block number. Our goal is to obtain transactions after this block number
            (if there are any).
            for_address (str): We are extracting transactions for this address.
        """

        logging.info(f"Extracting {for_address} since block: {block_height}")

        page_number = 0
        last_block_height = block_height
        latest_block_height = 0

        while True:

            response = self._request_transactions(for_address, page_number=page_number)
            block_height = self._covalent.get_block_height(response)

            if page_number == 0:
                latest_block_height = block_height

            # if block height is None, the extraction has finished or there are no
            # more transactions to extract
            # if block_height > last_block_height
            #   - loop through transactions adding them to our internal memory
            #     until block_height_txn <= last_block_height
            #   - if we have reached the end of items and we are still
            #     response_block_height > last_block_height, increment the page
            #     number and continue until block_height_txn <= last_block_height

            # nothing to update
            if block_height <= last_block_height:
                break

            # reached end of updates, or there are no transactions for the address
            if block_height == 0:
                break

            transactions = self._covalent.get_transactions(response)

            for txn in transactions:
                # * block height cannot be zero here due to the check earlier
                block_height = self._covalent.get_block_height_from_transaction(txn)
                if block_height > last_block_height:
                    self._transactions.append(txn)
                else:
                    break

            if block_height > last_block_height:
                page_number += 1
            else:
                break

        self._update_block_height(latest_block_height, for_address)

    # Interface Implementation

    def flush(self) -> None:

        if len(self._transactions) == 0:
            return

        # ! write transactions with `_load`

        self._transactions = []

    def extract(self) -> None:
        """
        Extracts transactions for all self._address
        """

        # Running this ensures we know what transactions to extract in the code
        # will follow. This avoids extracting all the transactions all the time.
        self._determine_block_height()

        # - check if the db has transactions, if it has, then download the new ones
        # if it doesn't have any transactions, download all
        # - we utilise a separate collection to track what raw transactions have
        # been extracted
        for addr in self._address:
            block_height = self._block_height[addr]
            self._extract_txn_history_since(block_height, addr)
