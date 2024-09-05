# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Methods to be called for parsing sovren resumes
@author <rchakraborty@simplifyvms.com>
"""
from abc import ABC

from datetime import date


class ResumeParserInterface(ABC):
    """
    Abstract class to implement job parsing operations
    """

    def get_result(
            self, request, service_name: str, index_id: str,
            document_as_base_64_string: str,
            resume_id: str, resume_document_id: str, job_id: str,
            name: str, first_name: str, last_name: str,
            email: str, phone: str, vendor: str,
            response_id: str, questions: str, score_required: str,
            api_source: str
    ) -> dict:
        """ pass """
        raise NotImplementedError()

    def connect_to_api(self, request, header: dict, payload: dict,
                       calling_api: str) -> dict:
        """ pass """
        raise NotImplementedError()

    def parse_resume(self, request, document_as_base_64_string: str, background_task: bool):
        """ pass """
        raise NotImplementedError()

    def call_sovren_parse_resume(self, request, base_64_encoded_string: str, revision_date: date,
                                 index_id: str, resume_document_id: str,
                                 resume_id: str, client_id: str, md5_hash: str,
                                 background_task:bool) -> dict:
        """ Pass """
        raise NotImplementedError()

    def delete_resume(self, request, resume_id: str, index_deletion: bool, resume_index: str) -> dict:
        """Delete Resume"""
        raise NotImplementedError()

    def connect_to_resume_deletion_api(self, request, header: dict, resume_index: str, resume_id: str,
                                       calling_api: str) -> dict:
        """ pass """
        raise NotImplementedError()

    def connect_to_index_deletion_api(self, request, header: dict, resume_index: str,
                                      calling_api: str) -> dict:
        """ pass """
        raise NotImplementedError()
