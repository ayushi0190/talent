# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Parsing Stats validations
@author <rchakraborty@simplifyvms.com>
@author <sreddy@simplifyvms.com>
"""
from typing import Optional, List
from pydantic import BaseModel, validator



class ParsingStatsValidations(BaseModel):
    """Parsing Stats"""

    parse_stats_for: str
    periods : int

    @validator("parse_stats_for")
    def parse_stats_for_must_be_string(cls, parse_stats_for):
        """
        Custom validation message for parse_stats_for
        :param v:
        :return:
        """
        if not isinstance(parse_stats_for, str):
            raise ValueError('Must be of string type')
        if parse_stats_for is None or len(parse_stats_for) == 0:
            raise ValueError('Parse Stats For can not be null')
        return parse_stats_for

    @validator("periods")
    def periods_must_be_integer(cls, periods):
        """
        Custom validation message for periods
        :param v:
        :return:
        """
        if not isinstance(periods, int):
            raise ValueError("Must be of integer type")
        if periods <= 0:
            raise ValueError('Periods Should be greaterthan 0')
        return periods


class AuditStatsValidations(BaseModel):
    """Audit Stats Validations"""

    service_name: str
    period : int

    @validator("service_name")
    def service_name_must_be_string(cls, service_name):
        """
        Custom validation message for service_name
        :param v:
        :return:
        """
        if not isinstance(service_name, str):
            raise ValueError('Must be of string type')
        if service_name is None or len(service_name) == 0:
            raise ValueError('Service Name can not be null')
        return service_name

    @validator("period")
    def period_must_be_integer(cls, period):
        """
        Custom validation message for period
        :param v:
        :return:
        """
        if not isinstance(period, int):
            raise ValueError("Must be of integer type")
        if period <= 0:
            raise ValueError('period Should be greaterthan 0')
        return period
