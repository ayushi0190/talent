
from abc import ABC


class ProfileInterface(ABC):
    """
    Abstract class to implement profile functionalities
    """

    def client_category_weights(self, request, data: dict) -> dict:
        """ pass """
        raise NotImplementedError()
