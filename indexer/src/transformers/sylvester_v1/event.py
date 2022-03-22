"""
This class defines ALL events generated by the Sylvester v1 contract.

Event List: Lend, Rent, StopRent, StopLend, RentClaimed
"""

import re
from abc import ABC
from dataclasses import asdict, dataclass
from typing import Any, List

from transformers.sylvester_v1.util import unpack_price


@dataclass
class SylvesterEvent(ABC):
    """
    Abstract Sylvester v1 Event. Holds txHash and txOffset, togther they are a unique 
    identifier for sylvester v1 events. e.i _id=txHash_txOffset
    """

    _id: str
    event: str

    def to_dict(self):
        """Return a dict representation of this event"""
        return asdict(self)


@dataclass
class LendEvent(SylvesterEvent):
    """
    LendEvent DTO

    Holds the event data for sylvester v1 'Lend' event.
    """

    # pylint: disable=invalid-name,too-many-instance-attributes
    is721: bool
    lenderAddress: str
    nftAddress: str
    tokenID: str
    lendingID: int
    maxRentDuration: int
    dailyRentPrice: float
    lendAmount: int
    paymentToken: int


   #TODO: Typing for event parameters
    @classmethod
    def from_covalent(cls, event: Any, decoded_params: List[Any]):
        """
        Parses a covalent event into a 'Lend' Sylvester v1 event.

        Args:
            event (Any): a covalent event
            decoded_params: (List[Any]): a list of decoded covalent event parameters. Order is important!

        Returns:
            _type_: instance of this class with the correct
            configs.
        """

        _id = f"{event['tx_hash']}_{event['log_offset']}"

        return cls(
            _id=_id,
            event='Lend',
            is721=decoded_params[0],
            lenderAddress=decoded_params[1],
            nftAddress=decoded_params[2],
            tokenID=decoded_params[3],
            lendingID=int(decoded_params[4]),
            maxRentDuration=int(decoded_params[5]),
            dailyRentPrice=unpack_price(decoded_params[6]),
            lendAmount=int(decoded_params[7]),
            paymentToken=int(decoded_params[8]),
        )


@dataclass
class RentEvent(SylvesterEvent):
    """
    RentEvent DTO

    Holds the event data for sylvester v1 'Rent' event.
    """

    # pylint: disable=invalid-name
    lendingID: int
    renterAddress: str
    rentDuration: int
    rentAmount: int
    rentingID: int
    rentedAt: int

   #TODO: Typing for event parameters
    @classmethod
    def from_covalent(cls, event: Any, decoded_params: List[Any]):
        """
        Parses a covalent event into a 'Rent' Sylvester v1 event.

        Args:
            event (Any): a covalent event
            decoded_params: (List[Any]): a list of decoded covalent event parameters. Order is important!

        Returns:
            _type_: instance of this class with the correct
            configs.
        """

        _id = f"{event['tx_hash']}_{event['log_offset']}"

        return cls(
            _id=_id,
            event='Rent',
            renterAddress=decoded_params[0],
            lendingID=int(decoded_params[1]),
            rentingID=int(decoded_params[2]),
            rentAmount=int(decoded_params[3]),
            rentDuration=int(decoded_params[4]),
            rentedAt=int(decoded_params[5])
        )


@dataclass
class StopRentEvent(SylvesterEvent):
    """
    StopRentEvent DTO

    Holds the event data for sylvester v1 'StopRent' event.
    """

    # pylint: disable=invalid-name
    rentingID: int
    stoppedAt: int

   #TODO: Typing for event parameters
    @classmethod
    def from_covalent(cls, event: Any, decoded_params: List[Any]):
        """
        Parses a covalent event into a 'StopRent' Sylvester v1 event.

        Args:
            event (Any): a covalent event
            decoded_params: (List[Any]): a list of decoded covalent event parameters. Order is important!

        Returns:
            _type_: instance of this class with the correct
            configs.
        """

        _id = f"{event['tx_hash']}_{event['log_offset']}"

        return cls(
            _id=_id,
            event='StopRent',
            rentingID=int(decoded_params[0]),
            stoppedAt=int(decoded_params[1]),
        )


@dataclass
class StopLendEvent(SylvesterEvent):
    """
    StopLendEvent DTO

    Holds the event data for sylvester v1 'StopLend' event.
    """

    # pylint: disable=invalid-name
    lendingID: int
    stoppedAt: int

   #TODO: Typing for event parameters
    @classmethod
    def from_covalent(cls, event: Any, decoded_params: List[Any]):
        """
        Parses a covalent event into a 'StopLend' Sylvester v1 event.

        Args:
            event (Any): a covalent event
            decoded_params: (List[Any]): a list of decoded covalent event parameters. Order is important!

        Returns:
            _type_: instance of this class with the correct
            configs.
        """

        _id = f"{event['tx_hash']}_{event['log_offset']}"

        return cls(
            _id=_id,
            event='StopLend',
            lendingID=int(decoded_params[0]),
            stoppedAt=int(decoded_params[1]),
        )


@dataclass
class RentClaimedEvent(SylvesterEvent):
    """
    RentClaimedEvent DTO

    Holds the event data for sylvester v1 'RentClaimed' event.
    """

    # pylint: disable=invalid-name
    rentingID: int
    collectedAt: int

   #TODO: Typing for event parameters
    @classmethod
    def from_covalent(cls, event: Any, decoded_params: List[Any]):
        """
        Parses a covalent event into a 'RentClaimed' Sylvester v1 event.

        Args:
            event (Any): a covalent event
            decoded_params: (List[Any]): a list of decoded covalent event parameters. Order is important!

        Returns:
            _type_: instance of this class with the correct
            configs.
        """

        _id = f"{event['tx_hash']}_{event['log_offset']}"

        return cls(
            _id=_id,
            event='RentClaimed',
            rentingID=int(decoded_params[0]),
            collectedAt=int(decoded_params[1]),
        )
