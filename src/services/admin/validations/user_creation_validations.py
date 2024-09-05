# coding:utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Searcher services validations
@author <rchakraborty@simplifyvms.com>
"""
from typing import Optional, List
from pydantic import BaseModel, validator


class UserCreationValidations(BaseModel):
    """ Search for Job or Resumes Based on Criteria """
    cmp_name: str
    clt_id: str
    cont_prd: int
    pool_inf: List[str]
    srv_prs : bool = True
    srv_mth : bool = True
    srv_src : bool = True
    srv_sco : bool = True
    prs_job : bool = True
    prs_res : bool = True
    sml_job : bool = True
    dis_can : bool = True
    sgt_can : bool = True
    sgt_job : bool = True
    cmp_can : bool = True
    get_res : bool = True
    get_job : bool = True
    src_job : bool = True
    sco_res : bool = True
