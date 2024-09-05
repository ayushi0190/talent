# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Methods to be called for searching resumes
@author <rchakraborty@simplifyvms.com>
"""
from abc import ABC, abstractmethod


class SearchJobResumeInterface(ABC):
    """
    Abstract class to implement searching resumes
    """

    @abstractmethod
    def get_search_jobs_resumes(self, request, data: object) -> dict:
        """ pass """

    @abstractmethod
    def connect_to_api(self, request, header: dict, calling_api: str,
                       payload: dict, applied_jobs: list, buckettype: str, count: int) -> dict:
        """ pass """
