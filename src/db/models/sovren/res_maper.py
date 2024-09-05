# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Resume mapper
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import DateTimeField, Document, StringField, BooleanField


class ResMapperModel(Document):
    """
    Map resume with resume bucket model
    """

    res_doc_id = StringField(required=False)
    res_idx_id = StringField(required=True)
    res_id = StringField(required=False)
    is_dup = BooleanField(required=False, default=False)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField()
