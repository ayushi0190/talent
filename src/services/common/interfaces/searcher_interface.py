# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Methods to be called for searching resumes
@author <rchakraborty@simplifyvms.com>
"""
from abc import ABC, abstractmethod


class SearcherInterface(ABC):
    """
    Abstract class to implement searching resumes
    """

    @abstractmethod
    def get_parsed_resume(self, data: dict) -> dict:
        """ pass """
