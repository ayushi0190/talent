# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Score By Id validations
@author <AnkitS@simplifyvms.com>
"""

from pydantic import BaseModel, validator
from typing import Optional, List

from src.services.common.config.common_config import common_url_settings

class ScoreByIdValidations(BaseModel):
    """
    Score for Job and Resumes
    """
    job_id: str
    resume_id: str
    job_category: Optional[str] = 'IT'
    category_weights: Optional[dict]
    parse_with: Optional[str] = 'sovren'

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

    @validator('resume_id')
    def resume_id_must_be_str(cls, resume_id):
        """
        Custom validation message for resume_id
        :param resume_id:
        :return:
        """
        if not isinstance(resume_id, str):
            raise ValueError('Must be of string type')
        if resume_id is None or len(resume_id) == 0:
            raise ValueError('Resume Id can not be null')
        return resume_id

    @validator('job_category')
    def job_category_must_be_str(cls, job_category):
        """
        Custom validation message for resume_id
        :param job_category:
        :return:
        """
        if not isinstance(job_category, str):
            raise ValueError('Must be of string type')
        return job_category

    @validator('category_weights')
    def category_weights_must_be_dict(cls, category_weights):
        """
        Custom validation message for resume_id
        :param category_weights:
        :return:
        """
        if not isinstance(category_weights, dict):
            raise ValueError('Must be of Dict type')
        return category_weights

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
