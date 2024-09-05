# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Methods to be called for Job Score
@author <AnkitS@simplifyvms.com>
"""
from abc import ABC


class ScorerInterface(ABC):
    """
    Abstract class to get Score
    """

    def get_result(
            self, request, resume_index_id: str, job_index_id: str,\
            job_id: str, resume_id: str
    ) -> dict:
        """ pass """
        raise NotImplementedError()

    def connect_to_api(self, request, header: dict, payload: dict,
                       calling_api: str) -> dict:
        """ pass """
        raise NotImplementedError()
