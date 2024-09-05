# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Get Parsing Stats for Resume and Job for Particular Client-Id
@author <sreddy@simplifyvms.com>
"""
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

import requests
from requests.exceptions import RequestException
from starlette.status import (HTTP_200_OK, HTTP_204_NO_CONTENT,
                              HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,HTTP_500_INTERNAL_SERVER_ERROR)

from src.db.crud.sovren.candidates_to_job_schema import CandidatesToJobSchema
from src.services.common.apis.job_board_services import JobBoardServices
from src.services.common.apis.matching_index_services import \
    MatchingIndexServices
from src.services.common.config.common_config import common_url_settings
from src.services.sovren.apis.job_parser_services import SovJobParserServices
from src.services.sovren.helpers.candidate_to_job_helper import wrap_matching_candidates
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.common.helpers.misc_helpers import (find_words_exists)
from src.services.sovren.helpers.misc_helpers import (get_sovren_headers, \
    data_with_no_of_matches, filter_fields_listing, get_job_index)
from src.services.sovren.helpers.search_job_resume_helpers import custom_all_filters
from src.services.sovren.interfaces.matchers.candidates_to_job_interface import \
    ICandidatesToJob
from src.services.common.helpers.misc_helpers import get_authorized_services
from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from src.db.crud.sovren.prs_jobs_inf_schema import PrsJobInfSchema
import datetime
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema
from src.admin.helpers.admin_helpers import find_field_name
from src.utilities.verify import service_url_check
class StatsAuditServices():
    """
    Audit Stats services class
    """

    def get_stat_audit(
            self, request, data: dict) -> List[Dict[str, Union[str, Any]]]:
        """
        Get Audit Stats Info
        :param data: Dictionary
        :return: Dict
        """
        from src.routes.main import url_list
        
        active_model = AuditTrailsSchema()
        response = {}
        extracted_data = {}
        clt_id = request.headers['client_id']
        service_name = data.get("service_name")
        if not(find_field_name(service_name)) and not(service_name == "All"):
            extracted_data.update(
                {
                    "code": HTTP_400_BAD_REQUEST,
                    "message": "Service name should be specified correctly",
                }
            )
            request.app.logger.debug(extracted_data)
            return extracted_data

        try:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=data.get("period"))).date()
            list_urls = [url.path for url in url_list[6:] if url.path not in common_url_settings.get("AUDIT_REMOVE_URLS")]
            list_urls = [url for url in list_urls if service_url_check(request,clt_id,url)]
            audit_list = active_model.get_data(clt_id,service_name,start_date)
            final_result = {}
            if audit_list:
                if service_name == common_url_settings.get("AUDIT_ALL"):
                    for ele in list_urls:
                        audit_count = sum([data.count for data in audit_list if data.service_name==ele])
                        final_result.update({
                            ele : audit_count
                        })
                else:
                    audit_count = sum([ele.count for ele in audit_list])
                    final_result.update({
                        data.get("service_name") : audit_count
                    })
                response.update({
                    "code" : HTTP_200_OK,
                    "data" : final_result
                })
            else:
                response.update({
                    'code': HTTP_400_BAD_REQUEST,
                    "message": "No Previous Request Made"
                })
            return response
        except Exception as ex:
            request.app.logger.info("Error in Audit Stats function %s " % str(ex))
            response.update({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error in retrieving Audit Stats function ",
                "error": "Exception is :" + str(ex)
            })
            return response
