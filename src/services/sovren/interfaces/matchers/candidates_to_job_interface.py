# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Methods to be called for job to jobs matcher services
@author <rchakraborty@simplifyvms.com>
"""
from abc import ABC


class ICandidatesToJob(ABC):
    """
    Abstract class to implement job to jobs functionalities
    """

    def get_result(self, request, data: dict) -> dict:
        """ pass """
        raise NotImplementedError()

    def jobs_finder(self, index_id: str, job_reference_num: str) -> list:
        """ pass """
        raise NotImplementedError()

    def connect_to_jobs_finder_api(
        self, header: dict, payload: dict, calling_api: str
    ) -> list:
        """ pass """
        raise NotImplementedError()
