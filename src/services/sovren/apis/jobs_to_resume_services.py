# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Get matching jobs for a given resume from sovren services
@author <rchakraborty@simplifyvms.com>
"""
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

import requests
from requests.exceptions import RequestException
from starlette.status import (HTTP_400_BAD_REQUEST,
                              HTTP_204_NO_CONTENT,HTTP_200_OK)

from src.db.crud.sovren.jobs_to_res_schema import JobsToResSchema
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.sovren.helpers.jobs_to_job_helpers import wrap_matching_jobs
from src.services.sovren.helpers.misc_helpers import get_sovren_headers, \
    get_resume_index, custom_all_filters, get_job_index_from_resume, data_with_no_of_matches, \
        filter_fields_listing
from src.services.sovren.interfaces.matchers.jobs_to_resume_interface import \
    JobsToResumeInterface
from src.services.common.config.common_config import common_url_settings
from src.services.sovren.helpers.search_job_resume_helpers import custom_all_filters
from src.db.crud.common.matching_index_schema import MatchingIndexSchema
from src.services.common.apis.matching_index_services import \
    MatchingIndexServices
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema

class JobsToResumeServices(JobsToResumeInterface):
    """
    Jobs to resume services class
    """

    def get_matched_jobs_to_resume(
            self, request, data: dict) -> List[Dict[str, Union[str, Any]]]:
        """
        Get list of jobs matching to a resume
        :param request: Request
        :param data: Dictionary
        :return: Dict
        """
        active_model = JobsToResSchema()
        clt_id = request.headers['client_id']
        data = filter_fields_listing(data)
        mat_index_schema = MatchingIndexSchema()
        audit_model = AuditTrailsSchema()
        service_name = request.url.path
        try:
            resume_bucket = (
                get_resume_index(data.get('resume_id'))
            )
            if len(data.get('bucket_source')) > 0:
                if data.get('bucket_source')[0] == 'All':
                    request_data = {
                        "index_type": sovren_url_settings.get("INDEX_TYPE_JOB")
                    }
                    index_matcher = MatchingIndexServices()
                    list_index = index_matcher.get_by_index_id_and_index_type(request_data)
                    job_bucket = [j.idx_id for j in list_index]
                else:
                    job_bucket = mat_index_schema.get_index_id_by_bucket_source_name(data.get("bucket_source"))
            searched_result = active_model.get_jobs(data.get('resume_id'), clt_id)
            if searched_result:
                time_since_last_transaction = datetime.now() - \
                                              searched_result.created_at
                if time_since_last_transaction.days > data.get('refresh_rate'):
                    del_prev_res = active_model.del_jobs(data.get('resume_id'), clt_id)
                    if del_prev_res:
                        searched_result = self.jobs_finder(resume_bucket,
                                                        job_bucket,
                                                        data.get('resume_id'),
                                                        data.get('no_of_matches'),
                                                        data.get('refresh_rate'),
                                                        data)
                        if searched_result.get('code') == HTTP_200_OK:
                            result = wrap_matching_jobs(searched_result.get('value'))
                            if len(result) > 0:
                                if len(data) == common_url_settings.get("MATCHER_CHECK_LENGTH"):
                                    active_model.add_searched_result(data.get('resume_id'),
                                                                    result, clt_id)
                        else:
                            return searched_result
                else:
                    if len(searched_result.srch_res) > 0:
                        if len(data) == common_url_settings.get("MATCHER_CHECK_LENGTH"):
                            result = searched_result.srch_res
                        else:
                            searched_result = self.jobs_finder(resume_bucket,
                                                            job_bucket,
                                                            data.get('resume_id'),
                                                            data.get('no_of_matches'),
                                                            data.get('refresh_rate'),
                                                            data)
                            if searched_result.get('code') == HTTP_200_OK:
                                result = wrap_matching_jobs(searched_result.get('value'))
                            else:
                                return searched_result
                    else:
                        searched_result = self.jobs_finder(resume_bucket,
                                                        job_bucket,
                                                        data.get('resume_id'),
                                                        data.get('no_of_matches'),
                                                        data.get('refresh_rate'),
                                                        data)
                        if searched_result.get('code') == HTTP_200_OK:
                            result = wrap_matching_jobs(searched_result.get('value'))
                            if len(result) > 0:
                                if len(data) == common_url_settings.get("MATCHER_CHECK_LENGTH"):
                                    active_model.add_searched_result(data.get('resume_id'),
                                                                    result, clt_id)
                        else:
                            return searched_result
            else:
                searched_result = self.jobs_finder(resume_bucket,
                                                   job_bucket,
                                                   data.get('resume_id'),
                                                   data.get('no_of_matches'),
                                                   data.get('refresh_rate'),
                                                   data)
                if searched_result.get('code') == HTTP_200_OK:
                    result = wrap_matching_jobs(searched_result.get('value'))
                    if len(result) > 0:
                        if len(data) == common_url_settings.get("MATCHER_CHECK_LENGTH"):
                            active_model.add_searched_result(data.get('resume_id'),
                                                            result, clt_id)
                else:
                    return searched_result
            result = data_with_no_of_matches(result, data)
            request.app.logger.info("Result {}".format(result))
            response = {}
            if len(result) > 0:
                response.update({
                    'code' : HTTP_200_OK,
                    'data' : result
                })
            else:
                response.update({
                    'code' : HTTP_204_NO_CONTENT,
                    'data' : result
                })
            audit_model.add(service_name,clt_id)
            return response
        except RequestException as e_msg:
            request.app.logger.error("Unable to get jobs against resume: '%s'" % e_msg)

    def jobs_finder(self, resume_index_id: str,
                    job_index_id: str,
                    resume_id: str,
                    no_of_matches: int,
                    refresh_rate: int,
                    data: dict) -> list:
        """
        Match's jobs with job and pull the result for client

        :param job_index_id: String
        :param resume_id: String
        :param data: Dictionary
        :param refresh_rate: Integer
        :param no_of_matches: Integer
        :param resume_index_id: String
        :return: Dict
        """
        current_date = datetime.today().strftime("%Y-%m-%d")
        date_minimum = datetime.today() - timedelta(
            days=int(refresh_rate)
        )
        payload = {
            "IndexIdsToSearchInto": job_index_id,
            "Take": no_of_matches,
            "FilterCriteria": {
                "RevisionDateRange": {
                    "Minimum": date_minimum.strftime("%Y-%m-%d"),
                    "Maximum": current_date,
                },
            },
        }
        payload = custom_all_filters(payload, data)
        calling_api = (
                sovren_url_settings.get("SOVREN_MATCH_DOCUMENT_BY_ID_URL")
                + resume_index_id
                + "/documents/"
                + resume_id
        )
        response = self.connect_to_jobs_finder_api(
            get_sovren_headers(), payload, calling_api
        )
        if not response:
            response.append({"code": HTTP_400_BAD_REQUEST})
        return response

    def connect_to_jobs_finder_api(
            self, header: dict, payload: dict, calling_api: str
    ) -> list:
        """
        Connect to Sovren and find similar jobs to a given job
        :param header:  Dictionary
        :param payload: Dictionary
        :param calling_api: String
        :return:
        """
        # global logger
        try:
            response = requests.request(
                "POST", url=calling_api, data=json.dumps(payload), headers=header
            )
            response_data = {}
            response_info = json.loads(json.dumps(response.json()))
            if response.status_code == HTTP_200_OK:
                response_data.update({
                    'code' : response.status_code,
                    'value' : response_info["Value"]["Matches"]
                })
            else:
                response_data.update({
                    'code' : response.status_code,
                    'value' : response_info.get("Info").get('Message')
                })
            return response_data
        except RequestException:
            pass
