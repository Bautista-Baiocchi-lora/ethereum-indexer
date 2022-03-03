from typing import Dict, List

from extract.covalent import Covalent as Covalent_


class Covalent(Covalent_):

    # todo: better txn type
    @staticmethod
    def decode(event: Dict) -> List:

        decoded = []

        # raw transaction log in case covalent failed to
        # decode some params
        raw_log_topics = event["raw_log_topics"]
        # covalent's attempt at decoding the log
        decoded_params = event["decoded"]["params"]

        for ix, decoded_param in enumerate(decoded_params):
            if decoded_param["decoded"] == True:
                decoded.append(decoded_param["value"])
            else:
                raw_param = raw_log_topics[ix + 1]

                if decoded_param["type"] == "uint256":
                    decoded.append(int(raw_param, 16))
                # todo: other types

        return decoded
