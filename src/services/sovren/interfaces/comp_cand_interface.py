# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Compare Candidate with job Validations
@author <AnkitS@simplifyvms.com>
"""

from abc import ABC, abstractmethod
from pydantic import BaseModel, validator


class CompareCandidateInput(BaseModel):
    """
    Compare Candidate with job Validations
    """
    JobId: str
    resume_id: list

    @validator('JobId')
    def job_id_must_be_string(cls, v):
        """
        Custom validation message for JobId
        :param v:
        :return:
        """
        if not isinstance(v, str):
            raise ValueError('Must be of string type')
        return v

    @validator('resume_id')
    def resume_id_must_be_list(cls, v):
        """
        Custom validation message for data
        :param v:
        :return:
        """
        if not isinstance(v, list):
            raise ValueError('Must be a list')
        return v

    @validator('JobId')
    def job_id_must_not_empty(cls, v):
        """
        Custom validation message for JobId
        :param v:
        :return:
        """
        for name in v:
            assert name != '', 'Empty strings are not allowed.'
        return v


class CompareCandidateInterface(ABC):
    """
       Abstract class to implement compare candidate against a JOB
       """

    @abstractmethod
    def list_compare_candidates_info_with_sovren(self, payload: dict) -> dict:
        """ Abstract CompareCandidateInterface"""
        raise NotImplementedError()
