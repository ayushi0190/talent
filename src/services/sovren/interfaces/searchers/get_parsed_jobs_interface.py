# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Methods to be called for searching resumes
@author <rchakraborty@simplifyvms.com>
"""
from abc import ABC, abstractmethod


class GetParsedJobsInterface(ABC):
    """
    Abstract class to implement Parsed Jobs
    """

    @abstractmethod
    def get_parsed_job(self, request, job_document_id: str) -> dict:
        """Get Result"""
        raise NotImplementedError()

    @abstractmethod
    def connect_to_api(self, request, header: dict, calling_api: str, job_document_id: str) -> dict:
        """Connect To API"""
        raise NotImplementedError()
