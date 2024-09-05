# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Define global types
@author <AnujY@simplifyvms.com>
"""
import typing

from pydantic import BaseModel


class ResponseBody(BaseModel):
    """ Common response model """
    code: int = None
    data: dict = None
    error: typing.Any = None
