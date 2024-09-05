# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Methods to be called for job board services
@author <rchakraborty@simplifyvms.com>
"""
from abc import ABC


class IJobBoard(ABC):
    """
    Abstract class to implement job board functionalities
    """

    def check_job_exist(self, request, job_id: str) -> dict:
        """ pass """
        raise NotImplementedError()

    def connect_to_job_board_api(self, request, header: dict, payload: dict,
                       calling_api: str) -> dict:
        """ pass """
        raise NotImplementedError()
