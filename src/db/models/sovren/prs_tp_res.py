# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Matched resume with Sovren from Talent Pool model
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import DateTimeField, Document, EmailField, StringField


class PrsTpResModel(Document):
    """
    Parse resume with sovren send from talent pool model
    """

    res_idx_id = StringField(required=True)
    resume = StringField(required=False)
    file_ext = StringField(required=False)
    res_b64 = StringField(required=False)
    res_std = StringField(required=False)
    res_id = StringField(required=False)
    res_doc_id = StringField(required=False)
    phone = StringField(required=False)
    name = StringField(required=False)
    f_name = StringField(required=False)
    l_name = StringField(required=False)
    email = EmailField(required=False)
    addr = StringField(required=False)
    clt_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField()
