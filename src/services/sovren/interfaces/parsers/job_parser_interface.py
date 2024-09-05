# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Methods to be called for parsing sovren jobs
@author <rchakraborty@simplifyvms.com>
"""
from abc import ABC


class JobParserInterface(ABC):
    """
    Abstract class to implement job parsing operations
    """

    def parse_with_job_board(self, data: dict) -> dict:
        """ pass """
        raise NotImplementedError()

    def connect_to_job_board_api(self, header: dict, payload: dict,
                                 calling_api: str) -> dict:
        """ pass """
        raise NotImplementedError()

    def parse_job(self, request, job_details:dict, data: dict) -> dict:
        """ pass """
        raise NotImplementedError()

    def connect_to_api(self, request, header: dict, payload: dict,
                       calling_api: str) -> dict:
        """ pass """
        raise NotImplementedError()

    def sovren_parse_job(self, request, job_document: str, job_index_id: str,
                         job_document_id: str, clt_id: str ) -> dict:
        """ pass """
        raise NotImplementedError()