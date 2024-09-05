# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Auth user model
@author <sreddy@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import DateTimeField, Document, StringField


class AuthModel(Document):
    """
    Find Candidates matching to a given job model
    """

    name = StringField(required=True)
    clt_id = StringField(required=True)
    auth_type = StringField(required=True)
    token = StringField(required=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()
