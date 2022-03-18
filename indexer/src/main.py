#!/usr/bin/env python
import logging
from multiprocessing import Process

from extract.main import Extract
from transform.main import Transform


def extract_and_load(address:str) -> None:
    extract = Extract(address)
    extract()

def transform_and_load(to_transform:str) -> None:
    transform = Transform(to_transform)
    transform()

def main():
    """Starts the whole ETL pipeline. Creates two separate processes.
    One for extraction, and one for transforming.
    """

    logging.basicConfig(
        filename="example_rumble_kong_league.log",
        level=logging.DEBUG,
        format="%(relativeCreated)6d %(process)d %(message)s",
    )

    to_transform = "example_rumble_kong_league"

    # rkl is the main rumble kong league collection
    # azrael is renft's v1 collateral solution
    # sylvester is renft's v1 collateral free solution
    # renft is a leading p2p nft rentals protocol
    address = "0xEf0182dc0574cd5874494a120750FD222FdB909a"

    # "0x94D8f036a0fbC216Bb532D33bDF6564157Af0cD7",  # azrael
    # "0xEf0182dc0574cd5874494a120750FD222FdB909a",  # rkl
    # "0xa8D3F65b6E2922fED1430b77aC2b557e1fa8DA4a",  # sylvester


    # todo: graceful keyboard interrupt
    extractor = Process(target=extract_and_load, args=[address])
    transformer = Process(target=transform_and_load, args=[to_transform])


    extractor.start()
    logging.info("Extractor started.")

    transformer.start()
    logging.info("Transformer started.")


if __name__ == "__main__":
    main()
