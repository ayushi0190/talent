# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Parse resume validations
@author <rchakraborty@simplifyvms.com>
"""

from pydantic import BaseModel, validator
from typing import Optional

from src.services.common.config.common_config import common_url_settings

class ParseProfileValidations(BaseModel):
    """
    Parse resume validations
    """
    document_as_base_64_string: str
    parse_with: str

    @validator("document_as_base_64_string")
    def document_as_base_64_string_must_be_str(cls, document_as_base_64_string):
        """
        Custom validation message for document_as_base_64_string
        :param document_as_base_64_string:
        :return:
        """
        if not isinstance(document_as_base_64_string, str):
            raise ValueError('Must be of string type')
        if document_as_base_64_string is None or len(document_as_base_64_string) == 0:
            raise ValueError('Base 64 String can not be null')
        return document_as_base_64_string

    @validator("parse_with")
    def parse_with_must_be_str(cls, parse_with):
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
        if parse_with is None or len(parse_with) == 0:
            raise ValueError('parse_with String can not be null')
        if parse_with.lower() not in service_names:
            raise ValueError('parse_with must be {}'
                             .format(' or '.join(service_names)))
        return parse_with