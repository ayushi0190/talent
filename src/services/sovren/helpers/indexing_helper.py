# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Miscellaneous helper methods
@author <rchakraborty@simplifyvms.com>
"""
import time
import random
import uuid
from src.services.common.apis.matching_index_services import MatchingIndexServices
from src.services.common.helpers.misc_helpers import find_words_exists
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.common.config.common_config import common_url_settings
from src.services.sovren.helpers.misc_helpers import error_in_indexing_result
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import requests
import json
from src.utilities.custom_logging import cust_logger as logger


def job_indexer(request, job_index_id: str) -> dict:
    """
    It will check whether Job index exist in DB or not
    If not then create Index in Sovren
    :param request
    :param resume_index_id:
    :return:
    """
    # Search whether index id of type "job" for this
    # job_id is present in database
    request_data = {"index_id": job_index_id, "index_type": sovren_url_settings.get("INDEX_TYPE_JOB")}
    index_matcher = MatchingIndexServices()
    job_index_exists = index_matcher.get_by_index_id_and_type(request_data)

    logger.info("JOB Index ID exist in DB %s " % job_index_exists)
    # If index not exist in DB then create index in Sovren
    if not job_index_exists:
        index_creation = index_matcher.create_index(request, job_index_id,
                                                    sovren_url_settings.get("INDEX_TYPE_JOB"))
        return index_creation
    else:
        return {
            "code": HTTP_200_OK,
            "message": "JOB Index already exist in DB",
            "data": ''
        }

def resume_indexer(request, resume_index_id: str) -> dict:
    """
    It will check whether Resume index exist in DB or not
    If not then create Index in Sovren
    :param request
    :param resume_index_id:
    :return:
    """
    # Search if index_id is present in our database and
    # thus make sure it is already exists in Sovren
    index_matcher = MatchingIndexServices()
    request_data = {"index_id": resume_index_id,
                    "index_type": sovren_url_settings.get("INDEX_TYPE_RESUME")}

    index_exists = index_matcher.get_by_index_id_and_type(request_data)
    logger.info("Resume Index ID exist in DB %s " % index_exists)
    # If index not exist in DB then create index in Sovren
    if not index_exists:
        index_creation = index_matcher.create_index(request, resume_index_id,
                                                    sovren_url_settings.get("INDEX_TYPE_RESUME"))
        return index_creation
    else:
        return {
            "code": HTTP_200_OK,
            "message": "Resume Index already exist in DB",
            "data": ''
        }
