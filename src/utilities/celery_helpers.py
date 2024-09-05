# -*- coding: utf-8 -*-
import json
from src.db.crud.sovren.cel_que_log_schema import CeleryQueLogSchema
from src.utilities.custom_logging import cust_logger as logger
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_304_NOT_MODIFIED


def add_celery_task_log(res_id: str, job_id: str, req_type: str, parser: str):
    celery_sch = CeleryQueLogSchema()
    add_task_req = {}
    add_task_req.update({
        "res_id": res_id,
        "job_id": job_id,
        "is_pros": False,
        "req_type": req_type,
        "clt_resp": "",
        "parser": parser
    })
    result = celery_sch.add_task(add_task_req)
    return result
    pass

def update_celery_task_log(res_id: str, job_id: str, req_type: str,
                           status: bool, resp: str, parser: str):
    celery_sch = CeleryQueLogSchema()
    data = {}
    data.update({
        "job_id": job_id,
        "res_id": res_id,
        "is_pros": status,
        "req_type": req_type,
        "clt_resp": resp,
        "parser": parser
    })
    
    result = celery_sch.update(data)
    return result
    pass
