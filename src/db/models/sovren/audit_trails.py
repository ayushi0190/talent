# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Matchers Stats
@author <ankits@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import DateField, Document, StringField, IntField


class AuditTrails(Document):
    """
    Audit Trails
    """

    service_name = StringField(required=True)
    client_id = StringField(required=True)
    count = IntField(required=True, default=0)
    proc_date = DateField(default=datetime.utcnow().date())
