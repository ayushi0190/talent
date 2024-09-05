# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Client registration model
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime

from mongoengine import DateTimeField, Document, StringField, IntField, BooleanField, ListField


class CltRegModel(Document):
    """
    User permission model
    """

    clt_name = StringField(required=True)  # Company name
    reg_dt = DateTimeField(required=True)  # Client registration date
    clt_id = StringField(required=True)  # Client id
    clt_res_idx_id = StringField(required=False)  # Client resume index id
    cont_prd = IntField(required=True, default=0)  # Contact period of the client
    pol_shr = BooleanField(required=True, default=True)  # Client agreed for shared pool
    pol_prv = BooleanField(required=True, default=True)  # Client agreed for private pool
    srv_prs = BooleanField(required=True, default=True)  # Client agreed for parsing services
    srv_mth = BooleanField(required=True, default=True)  # Client agreed for matcher services
    srv_src = BooleanField(required=True, default=True)  # Client agreed for searcher services
    srv_sco = BooleanField(required=True, default=True)  # Client agreed for scorer services
    prs_job = BooleanField(required=True, default=True)  # Parse job service enabled/disabled
    prs_res = BooleanField(required=True, default=True)  # Parse resume service enabled/disabled
    sml_job = BooleanField(required=True, default=True)  # Similar jobs service enabled/disabled
    dis_can = BooleanField(required=True, default=True)  # Discover candidates service enabled/disabled
    sgt_can = BooleanField(required=True, default=True)  # Suggested candidates service enabled/disabled
    sgt_job = BooleanField(required=True, default=True)  # Suggested jobs service enabled/disabled
    cmp_can = BooleanField(required=True, default=True)  # Compare candidates service enabled/disabled
    get_res = BooleanField(required=True, default=True)  # Get parsed resume service enabled/disabled
    get_job = BooleanField(required=True, default=True)  # Get parsed job service enabled/disabled
    src_job = BooleanField(required=True, default=True)  # Search job service enabled/disabled
    sco_res = BooleanField(required=True, default=True)  # Score resume to job service enabled/disabled
    tol_sov = BooleanField(required=True, default=True)  # Sovren pool to use enabled/disabled
    tol_ope = BooleanField(required=True, default=True)  # Opening.io pool to use enabled/disabled
    tol_sim = BooleanField(required=True, default=True)  # SimpAI pool to use enabled/disabled
    set_wgts = BooleanField(required=True, default=True)  # Category weight default settings enabled/disabled
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField()
