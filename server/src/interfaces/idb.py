"""
We use formal interfaces to enforce **modularity** first and foremost, and then structure
onto all of the code that is to be written.

Think of this as mathematical axioms, with which you then build proofs which you then use
together to build new proofs.
"""
import abc
from typing import Any

# todo: some of the items below can raise. Write docs for it


class IDB(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "get_item")
            and callable(subclass.get_item)
            or NotImplemented
        )

    @abc.abstractmethod
    def get_item(
        self, identifier: str, database_name: str, collection_name: str
    ) -> Any:
        """_summary_

        Args:
            identifier (str): the document '_id'
            database_name (str): name of the database
            collection_name (str): name of the collection

        Raises:
            NotImplementedError: _description_

        Returns:
            Any: _description_
        """
        raise NotImplementedError
