# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Matched resume with job score model
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime
from mongoengine import (Document,
                         StringField, DateTimeField)


class MpTpResModel(Document):
    """
    Mapped TalentPool resume with Sovren Model
    """
    res_idx_id = StringField(required=True)
    res = StringField(required=False)
    res_b64 = StringField(required=False)
    doc_id = StringField(required=False)
    clt_id = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField()
