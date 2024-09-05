# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Matched resume with job score model
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import DateTimeField, Document, StringField


class MatchJResScModel(Document):
    """
    Matched job resume response model
    """

    job_idx_id = StringField(required=True)
    job_id = StringField(required=True)
    res_idx_id = StringField(required=True)
    scr_res = StringField(required=False)
    res_id = StringField(required=True)
    clt_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()
    pars_typ = StringField(required=False)
