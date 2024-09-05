# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Methods to be called for searching resumes
@author <rchakraborty@simplifyvms.com>
"""
from abc import ABC, abstractmethod


class GetCandidateResumeInterface(ABC):
    """
    Abstract class to implement Parsed Jobs
    """

    @abstractmethod
    def get_candidate_resume(self, request, resume_id: str) -> dict:
        """Get Result"""
        raise NotImplementedError()
