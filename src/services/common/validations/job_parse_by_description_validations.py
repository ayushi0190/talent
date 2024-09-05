# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Parser services JobParserByDescription validations
@author <rchakraborty@simplifyvms.com>
"""
from typing import Optional, List

from pydantic import BaseModel, validator


class LocationDescriptionValidations(BaseModel):
    """
    Location Description Validations
    """
    country: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None

    @validator('country')
    def country_must_be_string(cls, country):
        """
        Custom validation message for country
        :param country:
        :return:
        """
        if not isinstance(country, str):
            raise ValueError('Must be of string type')
        return country

    @validator('city')
    def city_must_be_str(cls, city):
        """
        Custom validation message for city
        :param city:
        :return:
        """
        if not isinstance(city, str):
            raise ValueError('Must be of string type')
        return city

    @validator('state')
    def state_must_be_str(cls, state):
        """
        Custom validation message for state
        :param state:
        :return:
        """
        if not isinstance(state, str):
            raise ValueError('Must be of string type')
        return state

    @validator('zip')
    def zip_must_be_str(cls, zip):
        """
        Custom validation message for zip
        :param zip:
        :return:
        """
        if not isinstance(zip, str):
            raise ValueError('Must be of string type')
        return zip


class JobParseByDescriptionValidations(BaseModel):
    """
    Job parse by description validations
    """
    job_title: str
    job_description: str
    client_name: str
    work_location: List[LocationDescriptionValidations]

    @validator('job_title')
    def job_title_must_be_str(cls, job_title):
        """
        Custom validation message for job_title
        :param job_title:
        :return:
        """
        if not isinstance(job_title, str):
            raise ValueError('Must be of string type')
        if job_title is None or len(job_title) == 0:
            raise ValueError('Job Title can not be null')
        return job_title

    @validator('job_description')
    def job_description_must_be_str(cls, job_description):
        """
        Custom validation message for job_description
        :param job_description:
        :return:
        """
        if not isinstance(job_description, str):
            raise ValueError('Must be of string type')
        if job_description is None or len(job_description) == 0:
            raise ValueError('Job Description can not be null')
        return job_description

    @validator('work_location')
    def work_location_must_be_list(cls, work_location):
        """
        Custom validation message for work_location
        :param work_location:
        :return:
        """
        if not isinstance(work_location, list):
            raise ValueError('Must be of list type')
        return work_location
