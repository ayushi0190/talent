# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Parse jobs with sovren model
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import DateTimeField, Document, StringField, IntField


class PrsJobInfModel(Document):
    """
    Parse Job Information in Sovren Model



    index_id = StringField(required=True)
    job_id = StringField(required=True)
    sor_sys = StringField(required=False)
    sor_tp = StringField(required=False)
    sor_prod = StringField(required=False)
    clt_job_id = StringField(required=False)
    job_brd_id = StringField(required=False)
    job_res = StringField(required=True)
    clt_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField()
    """

    index_id = StringField(required=True)
    job_id = StringField(required=True)
    job_res = StringField(required=True)
    clt_id = StringField(required=True)
    norm_resp = StringField(required=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()
    prs_time = IntField(required=True, default=0)
    pars_typ = StringField(required=False)
