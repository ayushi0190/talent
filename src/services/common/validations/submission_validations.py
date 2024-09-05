# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Submissions validations
@author <rchakraborty@simplifyvms.com>
"""
from typing import Optional

from pydantic import BaseModel, validator
from src.services.common.config.common_config import common_url_settings


class SubmissionValidations(BaseModel):
    """Resume parsing validations"""
    document_as_base_64_string: str
    job_id: str
    name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    vendor: Optional[str] = None
    response_id: Optional[str] = None
    questions: Optional[list]
    score_required: Optional[list] = []
    api_source: Optional[str] = None
    additional_skills: Optional[list] = []
    parse_with: Optional[str] = 'sovren'

    @validator("document_as_base_64_string")
    def document_as_base_64_string_must_be_str(cls, document_as_base_64_string):
        """
        Custom validation message for document_as_base_64_string
        :param document_as_base_64_string:
        :return:
        """
        if not isinstance(document_as_base_64_string, str):
            raise ValueError("Must be of string type")
        return document_as_base_64_string

    @validator('job_id')
    def job_id_must_be_str(cls, job_id):
        """
        Custom validation message for job_id
        :param job_id:
        :return:
        """
        if not isinstance(job_id, str):
            raise ValueError('Must be of string type')
        if job_id is None or len(job_id) == 0:
            raise ValueError('Job Id can not be null')
        return job_id

    @validator('score_required')
    def score_required_must_be_str(cls, score_required):
        """
        Custom validation message for score_required
        :param score_required:
        :return:
        """
        if not isinstance(score_required, list):
            raise ValueError('Must be of list type')
        service_names = [common_url_settings.get('SOVREN_SERVICE'),
                        common_url_settings.get('SIMPAI_SERVICE')]
        if len(score_required)  == 0:
            raise ValueError('score_required must contain {}'
                             .format(' or '.join(service_names)))
        return score_required

    @validator('api_source')
    def api_source_must_be_str(cls, api_source):
        """
        Custom validation message for api_source
        :param api_source:
        :return:
        """
        if not isinstance(api_source, str):
            raise ValueError('Must be of string type')
        if api_source is None or len(api_source) == 0:
            raise ValueError('api source can not be null')
        return api_source

    @validator("parse_with")
    def parse_with_must_be_valid(cls, parse_with):
        """
        Custom validation message for parse_with
        :param parse_with:
        :return:
        """
        service_names = ['default',
                        common_url_settings.get('SOVREN_SERVICE'),
                        common_url_settings.get('SIMPAI_SERVICE'),
                        common_url_settings.get('OPENING_SERVICE')
                        ]
        if not isinstance(parse_with, str):
            raise ValueError('Must be of string type')
        if parse_with.lower() not in service_names:
            raise ValueError('parse_with must be {}'
                             .format(' or '.join(service_names)))
        return parse_with
