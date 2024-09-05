# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Parser services JobParserByIdValidations validations
@author <rchakraborty@simplifyvms.com>
"""
from pydantic import BaseModel, validator
from typing import Optional, List

from src.services.common.config.common_config import common_url_settings

class JobParseByIdValidations(BaseModel):
    """Validations Class for Job Parsing with Id"""
    job_id: str
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
