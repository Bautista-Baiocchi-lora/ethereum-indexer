#!/usr/bin/env python
import logging
import sys
from multiprocessing import Process

from config import Config
from extract.main import Extract
from transform.main import Transform


def extract_and_load(address: str) -> None:
    """
    Initiate and start extractor process.

    Args:
        address (str): Target wallet address for extractor
    """

    extract = Extract(address)
    extract()

def transform_and_load(to_transform: str) -> None:
    """
    Initiate and start transformer process.

    Args:
        to_transform (str): Transformer sub-directory name to be instantiated
    """

    transform = Transform(to_transform)
    transform()

def main():
    """Starts the whole ETL pipeline. Creates two separate processes.
    One for extraction, and one for transforming.
    """

    config = Config.azrael()

    logging.basicConfig(
        filename=config.get_log_filename(),
        level=logging.INFO,
        format="%(relativeCreated)6d %(process)d %(message)s",
    )

    # rkl is the main rumble kong league collection
    # azrael is renft's v1 collateral solution
    # sylvester is renft's v1 collateral free solution
    # renft is a leading p2p nft rentals protocol

    # "0x94D8f036a0fbC216Bb532D33bDF6564157Af0cD7",  # azrael
    # "0xEf0182dc0574cd5874494a120750FD222FdB909a",  # rkl
    # "0xa8D3F65b6E2922fED1430b77aC2b557e1fa8DA4a",  # sylvester


    # todo: graceful keyboard interrupt
    extractor = Process(target=extract_and_load, args=[config])
    transformer = Process(target=transform_and_load, args=[config])


    extractor.start()
    logging.info("Extractor started.")

    transformer.start()
    logging.info("Transformer started.")


    extractor.join() # wait to finish
    transformer.join() # wait to finish



if __name__ == "__main__":
    sys.exit(main())
