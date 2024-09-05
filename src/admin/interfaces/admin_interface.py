
from abc import ABC


class AdminInterface(ABC):
    """
    Abstract class to implement admin functionalities
    """

    def register_client(self, request, data: dict) -> dict:
        """ pass """
        raise NotImplementedError()