from typing import Dict

from extract.covalent import Covalent as Covalent_


class Covalent(Covalent_):
    """@inheritdoc Covalent"""

    # todo: better txn type
    # TODO: Support more types
    @staticmethod
    def decode(event: Dict) -> Dict:
        """Decodes Covalent blockchain event into Dict. Takes care of casting
        solidity types to proper pythonic types.

        Args:
            event (Dict): Covalent blockchain event.

        Returns:
            Dict: name to value mapping.
        """

        decoded = {}

        # raw transaction log in case covalent failed to
        # decode some params
        raw_log_topics = event["raw_log_topics"]
        # covalent's attempt at decoding the log
        decoded_params = event["decoded"]["params"]

        for ix, decoded_param in enumerate(decoded_params):
            if decoded_param["decoded"] is True:
                decoded[decoded_param["name"]] = decoded_param["value"]
            else:
                raw_param = raw_log_topics[ix + 1]

                if decoded_param["type"] == "uint256":
                    decoded[decoded_param["name"]] = int(raw_param, 16)
                # TODO: Other types
                else:
                    raise NotImplementedError(
                        f'Undecoded covalent param: {decoded_param["type"]}'
                    )

        return decoded
