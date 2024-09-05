# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Category wise weight's registration model
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import DateTimeField, Document, StringField, ListField, DictField


class CltCatWgtModel(Document):
    """
    Category wise weight registration
    """

    clt_id = StringField(required=True)  # Client id
    job_category = StringField(required=True)  # Job Category
    cat_weights = DictField(required=True, default=True)  # Dict of category weights
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()

class CltCatWgtModel_Old(Document):
    """
    Category wise weight registration
    """

    clt_id = StringField(required=True)  # Client id
    job_category = StringField(required=True)  # Job Category
    categories = ListField(required=True, default=True)  # Client agreed to provide categories
    weights = ListField(required=True, default=True)  # Client agreed to provide weights
    created_at = DateTimeField(default=datetime.utcnow())
    updated_at = DateTimeField()
