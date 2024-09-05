# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Parse resume information with Sovren model for INTERNAL BUCKET
@author <ankits@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import DateTimeField, Document, StringField, IntField, ListField


class InternResModel(Document):
    """
    Parse Resume Information in Sovren Model fro INTERNAL BUCKET
    """

    idx_id = StringField(required=True)
    res_doc_id = StringField(required=True)
    doc_md5 = StringField(required=True)
    res_id = StringField(required=True)
    resp = StringField(required=False)
    clt_id = StringField(required=True)
    norm_resp = StringField(required=False)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()
    res_b64 = StringField(required=False)
    prs_time = IntField(required=True, default=0)
    orig_doc_md5 = StringField(required=False)
    additional_skills = ListField(required=False)
    pars_typ = StringField(required=False)
