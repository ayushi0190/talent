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

class StatsParsingServices():
    """
    Parsing Stats services class
    """

    def get_stat_parsing(
            self, request, data: dict) -> List[Dict[str, Union[str, Any]]]:
        """
        Get Parsing Stats Info
        :param data: Dictionary
        :return: Dict
        """
        response = {}
        extracted_data = {}
        clt_id = request.headers['client_id']
        parse_stats_for = data.get("parse_stats_for").capitalize()
        if parse_stats_for not in [sovren_url_settings.get("INDEX_TYPE_RESUME"),sovren_url_settings.get("INDEX_TYPE_JOB"),common_url_settings.get("AUDIT_ALL")]:
            extracted_data.update(
                {
                    "code": HTTP_400_BAD_REQUEST,
                    "message": "Provide Job/Resume/All as argument in your payload for parse_stats_for",
                }
            )
            request.app.logger.debug(extracted_data)
            return extracted_data
        
        try:
            start_date = datetime.datetime.now() - datetime.timedelta(days=data.get("periods"))
            if parse_stats_for == sovren_url_settings.get("INDEX_TYPE_JOB"):
                job_model = PrsJobInfSchema()
                stat_data = job_model.get_stat_job(request, clt_id, start_date)
                if stat_data:
                    response.update({
                        "code" : HTTP_200_OK,
                        'count' : stat_data[0],
                        'jobs' : stat_data[1]
                    })

                else:
                    response.update({
                        "code" : HTTP_204_NO_CONTENT,
                        "count" : 0,
                        'jobs' : []
                    })
                request.app.logger.info("Parsed Jobs Count %s " % str(response['count']))
                request.app.logger.info("Parsed Jobs Ids %s " % str(response['jobs']))
            elif parse_stats_for == sovren_url_settings.get("INDEX_TYPE_RESUME"):
                resume_model = PrsResInfSchema()
                stat_data = resume_model.get_stat_resumes(request, clt_id, start_date)
                if stat_data:
                    response.update({
                        "code" : HTTP_200_OK,
                        'count' : stat_data[0],
                        'resumes' : stat_data[1]
                    })

                else:
                    response.update({
                        "code" : HTTP_204_NO_CONTENT,
                        "count" : 0,
                        'resumes' : []
                    })
                request.app.logger.info("Parsed Resumes Count %s " % str(response['count']))
                request.app.logger.info("Parsed Resumes Ids %s " % str(response['resumes']))
            elif parse_stats_for == common_url_settings.get("AUDIT_ALL"):
                resume_model = PrsResInfSchema()
                res_stat_data = resume_model.get_stat_resumes(request, clt_id, start_date)
                job_model = PrsJobInfSchema()
                job_stat_data = job_model.get_stat_job(request, clt_id, start_date)
                response.update({
                    "code" : ""
                })
                if res_stat_data:
                    response.update({
                        "resume_count": res_stat_data[0],
                        "resumes": res_stat_data[1]
                    })
                if job_stat_data:
                    response.update({
                        "job_count": job_stat_data[0],
                        "jobs": job_stat_data[1]
                    })
                if response:
                    response.update({
                        'code' : HTTP_200_OK
                    })
                else:
                    response.update({
                        "code" : HTTP_204_NO_CONTENT,
                        "count" : 0
                    })
            return response
        except Exception as ex:
            request.app.logger.info("Error in Parsing Stats function %s " % str(ex))
            response.update({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error in retrieving Parsing Stats function ",
                "error": "Exception is :" + str(ex)
            })
            return response
