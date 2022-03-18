#!/usr/bin/env python
from multiprocessing import Process
import logging

from extract.main import Extract
from transform.main import Transform
from config import Config


def main():
    """Starts the whole ETL pipeline. Creates two separate processes.
    One for extraction, and one for transforming.
    """

    config = Config.rkl_club_auction()

    logging.basicConfig(
        filename=config.get_log_filename(),
        level=logging.DEBUG,
        format="%(relativeCreated)6d %(process)d %(message)s",
    )

    def extract_and_load():
        extract = Extract(config.get_address())
        extract()

    def transform_and_load():
        transform = Transform(config.get_transformer_name())
        transform()

    # todo: graceful keyboard interrupt
    p1 = Process(target=extract_and_load)
    p1.start()
    p1.join()

    p2 = Process(target=transform_and_load)
    p2.start()
    p2.join()


if __name__ == "__main__":
    main()
