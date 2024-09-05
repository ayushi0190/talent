# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Parse resume with sovren called from SimplifyHire model
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import (BooleanField, DateTimeField, Document, EmailField,
                         StringField)


class ResSimpHireModel(Document):
    """
    Parse Resume with Sovren called from SimplifyHire Model
    """

    res_idx_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField()
    phone = StringField(required=False)
    name = StringField(required=False)
    f_name = StringField(required=False)
    l_name = StringField(required=False)
    email = EmailField(required=False)
    vendor = StringField(required=False)
    resume = StringField(required=False)
    res_std = StringField(required=False)
    res_doc_id = StringField(required=False)
    srch_res = StringField(required=False)
    res_sent = BooleanField(required=False)
