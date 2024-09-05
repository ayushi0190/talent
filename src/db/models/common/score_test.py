# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Matching indexes model
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import DateTimeField, Document, StringField, DictField


class ScoreTestModel(Document):
    """ ScoreTestModel """

    created_at = DateTimeField(default=datetime.utcnow())
    score_resp = DictField()
