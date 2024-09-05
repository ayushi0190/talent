# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Handle exception
@author <AnujY@simplifyvms.com>
"""


class APIException(Exception):
    """
    Handle exception
    """
    def __init__(self, value):
        Exception.__init__(self, value)
        self.msg = value

    def __str__(self):
        return repr(self.msg)
