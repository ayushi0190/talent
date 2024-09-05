# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Sovren score sending queue log model
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import (BooleanField, DateTimeField, Document, LongField,
                         StringField)


class CeleryQueLogModel(Document):
    """
    Sovren score sending queue log model
    """

    job_id = StringField(required=True)
    res_id = StringField(required=True)
    is_pros = BooleanField(required=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    clt_resp = StringField(required=False)
    req_type = StringField(required=False)
    pars_typ = StringField(required=False)
