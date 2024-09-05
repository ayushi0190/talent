# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Methods to be called for matching indexes services
@author <rchakraborty@simplifyvms.com>
"""
from abc import ABC


class IMatchingIndex(ABC):
    """
    Abstract class to implement matching indexes operations
    """

    def get_by_index_id_and_type(self, data: dict) -> dict:
        """ pass """
        raise NotImplementedError()


    def create_index(self, request, index_id: str, index_type: str) -> dict:
        """
         Create Index from Sovren and Save to DB
        :param index_id: String
        :param index_type: String
        :return:

        """
        """ pass """
        raise NotImplementedError()

    def connect_to_api(self, request, header: dict, payload: dict,
                       calling_api: str) -> dict:
        """

        Call Sovren API to create Index
        :param header: Dictionary
        :param payload: Dictionary
        :param calling_api: String
        :return: JSON
        
        """

        """ pass """
        raise NotImplementedError()


    def get_by_index_id_and_index_type(self, data: dict) -> dict:
        """ pass """
        raise NotImplementedError()
