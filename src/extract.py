"""Responsible for extracting the raw transaction data for the address"""
from typing import List
import time

from interfaces.iextract import IExtract
from load import Load


class Extract(IExtract):
    """
    The job of extractor is to extract all the historical raw transaction
    data pertaining to an address and check for any new transactions
    concerning the said addresses every update_frequency.

    The said transactions are stored in memory until loader takes them
    and writes to the db. Upon successful write, they are removed from memory.
    """

    def __init__(self, address: List[str], update_frequency: List[int]):
        """
        @param address: list of addresses for which to extract the raw historical
        transaction data.
        @param update_frequency: list of update frequencies for each of the
        addresses supplied.
        """
        # Validate the addresses. https://github.com/ethereum/web3.py/blob/71ef3cd7edc299be64a8767c2a354a56c552555c/tests/core/utilities/test_validation.py#L11
        # Store the address
        self._validate_address(address)
        self._validate_update_frequency(update_frequency)

        self._address: List[str] = self._strandardise_address(address)
        self._update_frequency: List[int] = update_frequency

        self._load = Load()

    def _validate_address(self, address: List[str]):
        """
        Raises if any address is invalid.
        """
        ...

    def _validate_update_frequency(self, update_frequency: List[int]):
        """
        Raises if any update frequency is invalid.
        """
        ...

    def _strandardise_address(self, address: List[str]) -> List[str]:
        """
        Standardises the address as per ...
        """
        ...

    def is_connected_to_internet(self) -> bool:
        """Determines if connected to Internet"""
        return True

    def flush(self):
        return

    def extract(self):
        time.sleep(1)
        return
