# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Contact information from talent pool model
@author <rchakraborty@simplifyvms.com>
"""

from mongoengine import Document, StringField


class CntTpModel(Document):
    """
    Contact information from talent pool model
    """
    res_id = StringField(required=False)
    CntInf = StringField(required=False)
