# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Opening score sending queue log model
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import (BooleanField, DateTimeField, Document, LongField,
                         StringField)


class OpProLogsModel(Document):
    """
    Opening score sending queue log model
    """

    job_res_id = LongField(required=True)
    is_pros = BooleanField(required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField()
    clt_res = StringField(required=False)
