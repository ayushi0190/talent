# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Find candidates matching to a given job model
@author <rchakraborty@simplifyvms.com>
@author <sreddy@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import DateTimeField, Document, ListField, StringField


class CandToJobModel(Document):
    """
    Find Candidates matching to a given job model
    """

    job_id = StringField(required=True)
    srch_res = ListField(required=False)
    clt_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField()
