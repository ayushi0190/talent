# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Submission information
@author <ankits@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import DateTimeField, Document, StringField, ListField


class SubmissionInfModel(Document):
    """
    Parse Resume Information in Sovren Model
    """

    idx_id = StringField(required=True)
    res_doc_id = StringField(required=True)
    res_id = StringField(required=True)
    clt_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()
    job_id = StringField(required=True)
    name = StringField(required=False)
    first_name = StringField(required=False)
    last_name = StringField(required=False)
    email = StringField(required=False)
    phone = StringField(required=False)
    vendor = StringField(required=False)
    response_id = StringField(required=False)
    questions = ListField(required=False)
    score_required = ListField(required=False)
    api_source = StringField(required=False)
    pars_typ = StringField(required=False)
