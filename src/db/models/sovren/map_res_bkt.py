# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Map resume with resume bucket
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import DateTimeField, Document, StringField, BooleanField


class MapResBktModel(Document):
    """
    Map resume with resume bucket model
    """

    res_doc_id = StringField(required=False)
    prs_res = StringField(required=False)
    scr_gen = BooleanField(required=False, default=True)
    clt_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()
