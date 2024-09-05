# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Methods to be called for Submission
@author <AnkitS@simplifyvms.com>
"""
from abc import ABC


class SubmissionInterface(ABC):
    """
    Abstract class for Submission
    """

    def call_submission(
            self, request,
            document_as_base_64_string: str,
            job_id: str, name: str, first_name: str, last_name: str,
            email: str, phone: str, vendor: str,
            response_id: str, questions: list, score_required: str,
            api_source: str
    ) -> dict:
        """ pass """
        raise NotImplementedError()

