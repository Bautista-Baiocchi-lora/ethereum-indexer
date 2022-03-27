"""
This class defines ALL events generated by the sylvester contract.

Event List: Lend, Rent, StopRent, StopLend, RentClaimed
"""

import re
from abc import ABC
from dataclasses import asdict, dataclass
from typing import Any, List, Union

ID_SEPERATOR='_'

@dataclass
class SylvesterEvent(ABC):
    """
    Abstract sylvester Event. Holds txHash and txOffset, togther they are a unique
    identifier for sylvester events. e.i _id=txHash_txOffset
    """

    _id: str
    event: str


    @staticmethod
    def get_id(tx_hash: str, tx_offset: Union[str, int]) -> str:
        """Creates unique identifier for Sylvester Event
        
        Args:
            tx_hash (str): transaction hash
            tx_offset (Union[str, int]): transaction offset

        Returns:
            id (str): Unique identifier composed of txHash and txOffset.
                e.i. 0xf79edc5500218427d22d4215799fb51064c633ca919c0406b830ed5dc3c6eb1a_100
        """
        return f"{tx_hash}{ID_SEPERATOR}{tx_offset}"

    def to_dict(self):
        """Return a dict representation of this event"""
        return asdict(self)


@dataclass
class LendEvent(SylvesterEvent):
    """
    LendEvent DTO (Data Transfer Object)

    Holds the event data for sylvester 'Lend' event.
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
    #pylint: disable=too-many-arguments
    @classmethod
    def create(
        cls,
        tx_hash: str,
        log_offset: Union[int, str],
        is_721: bool,
        lender_address: str,
        nft_address: str,
        token_id: str,
        lending_id: int,
        max_rent_duration: int,
        daily_rent_price: int,
        lend_amount: int,
        payment_token: int
    ):
        """
        Factory method for 'Lend' sylvester event.

        Args:
            tx_hash (str): The hash of the transaction
            log_offset (str): The offset of the transaction
            nft_address (str): Address of NFT to be lent
            token_id (str): Id of NFT being lent
            lend_amount (int): Amount of NFT of token_id to be lent
            lending_id (int): Id of the ReNFT lending
            lender_address (str): Wallet address of lender
            max_rent_duration (int): Maximum rent duration in days
            daily_rent_price (int): Daily rental price for NFT, denominated in payment_token
            is_721 (bool): True if NFT being lent is ERC721, False if NFT is ERC1155
            payment_token (int): Token to be used for rental payment

        Returns:
            (LendEvent): instance of this class with the correct
            configs.
        """

        _id = SylvesterEvent.get_id(tx_hash, log_offset)

        return cls(
            _id=_id,
            event='Lend',
            is721=is_721,
            lenderAddress=lender_address,
            nftAddress=nft_address,
            tokenID=token_id,
            lendingID=lending_id,
            maxRentDuration=max_rent_duration,
            dailyRentPrice=daily_rent_price,
            lendAmount=lend_amount,
            paymentToken=payment_token,
        )


@dataclass
class RentEvent(SylvesterEvent):
    """
    RentEvent DTO (Data Transfer Object)

    Holds the event data for sylvester 'Rent' event.
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
    def create(cls, 
        tx_hash: str,
        log_offset: Union[str, int],
        lending_id: int,
        renter_address: int,
        renting_id: int,
        rent_amount: int,
        rent_duration: int,
        rented_at: int
        ):
        """
        Factory method for 'Rent' sylvester event.

        Args:
            tx_hash (str): The hash of the transaction
            log_offset (str): The offset of the transaction
            lending_id (int): Id of the ReNFT lending
            renting_id (int): Id of ReNFT renting
            renter_address (str): Wallet address of renter
            rent_duration (int): Duration of rental in days
            rented_at (int): Block timestamp of the transaction

        Returns:
            (RentEvent): instance of this class with the correct
            configs.
        """

        _id = SylvesterEvent.get_id(tx_hash, log_offset)

        return cls(
            _id=_id,
            event='Rent',
            renterAddress=renter_address,
            lendingID=lending_id,
            rentingID=renting_id,
            rentAmount=rent_amount,
            rentDuration=rent_duration,
            rentedAt=rented_at
        )


@dataclass
class StopRentEvent(SylvesterEvent):
    """
    StopRentEvent DTO (Data Transfer Object)

    Holds the event data for sylvester 'StopRent' event.
    """

    # pylint: disable=invalid-name
    rentingID: int
    stoppedAt: int

    #TODO: Typing for event parameters
    @classmethod
    def create(cls, tx_hash: str, log_offset: Union[str, int], renting_id: int, stopped_at: int):
        """
        Factory method for 'StopRent' sylvester event.

        Args:
            tx_hash (str): The hash of the transaction
            log_offset (str): The offset of the transaction
            renting_id (int): Id of ReNFT renting
            stopped_at (int): Block timestamp of the transaction

        Returns:
            (StopRentEvent): instance of this class with the correct
            configs.
        """

        _id = SylvesterEvent.get_id(tx_hash, log_offset)

        return cls(
            _id=_id,
            event='StopRent',
            rentingID=renting_id,
            stoppedAt=stopped_at,
        )


@dataclass
class StopLendEvent(SylvesterEvent):
    """
    StopLendEvent DTO (Data Transfer Object)

    Holds the event data for sylvester 'StopLend' event.
    """

    # pylint: disable=invalid-name
    lendingID: int
    stoppedAt: int

   #TODO: Typing for event parameters
    @classmethod
    def create(cls, tx_hash: str, log_offset: Union[str, int], lending_id: int, stopped_at: int):
        """
        Factory method for 'StopLend' sylvester event.

        Args:
            tx_hash (str): The hash of the transaction
            log_offset (str): The offset of the transaction
            lending_id (int): Id of ReNFT lending
            stopped_at (int): Block timestamp of the transaction

        Returns:
            (StopLendEvent): instance of this class with the correct
            configs.
        """

        _id = SylvesterEvent.get_id(tx_hash, log_offset)

        return cls(
            _id=_id,
            event='StopLend',
            lendingID=lending_id,
            stoppedAt=stopped_at,
        )


@dataclass
class RentClaimedEvent(SylvesterEvent):
    """
    RentClaimedEvent DTO (Data Transfer Object)

    Holds the event data for sylvester 'RentClaimed' event.
    """

    # pylint: disable=invalid-name
    rentingID: int
    collectedAt: int

   #TODO: Typing for event parameters
    @classmethod
    def create(cls, tx_hash: str, log_offset: Union[str, int], renting_id: int, collected_at: int):
        """
        Factory method for 'RentClaimed' sylvester event.

        Args:
            tx_hash (str): The hash of the transaction
            log_offset (str): The offset of the transaction
            renting_id (int): Id of ReNFT renting
            collected_at (int): Block timestamp of the transaction

        Returns:
            (RentClaimedEvent): instance of this class with the correct
            configs.
        """

        _id = SylvesterEvent.get_id(tx_hash, log_offset)

        return cls(
            _id=_id,
            event='RentClaimed',
            rentingID=renting_id,
            collectedAt=collected_at,
        )