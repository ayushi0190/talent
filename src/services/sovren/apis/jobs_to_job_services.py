# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Get matching jobs for a given job from sovren services
@author <rchakraborty@simplifyvms.com>
"""
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

import requests
from requests.exceptions import RequestException
from starlette.status import (HTTP_200_OK, HTTP_204_NO_CONTENT,
                              HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)

from src.db.crud.sovren.job_to_jobs_schema import JobsToJobSchema
from src.services.common.apis.job_board_services import JobBoardServices
from src.services.common.apis.matching_index_services import \
    MatchingIndexServices
from src.services.common.helpers.misc_helpers import find_words_exists
from src.services.sovren.apis.job_parser_services import SovJobParserServices
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.sovren.helpers.jobs_to_job_helpers import wrap_matching_jobs, jobs_to_job_filters
from src.services.sovren.helpers.misc_helpers import get_job_index
from src.services.sovren.helpers.misc_helpers import get_sovren_headers, filter_fields_listing, \
    data_with_no_of_matches
from src.services.sovren.interfaces.matchers.job_to_jobs_interface import \
    IJobToJobs
from src.services.sovren.helpers.search_job_resume_helpers import custom_all_filters
from src.services.common.config.common_config import common_url_settings
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema

class JobToJobsServices(IJobToJobs):
    """
    Job to jobs services class
    """

    def get_matched_jobs(
            self, request, data: dict) -> List[Dict[str, Union[str, Any]]]:
        """
        Get list of jobs matching to a job
        :param request: Request
        :param data: Dictionary
        :return: Dict
        """
        active_model = JobsToJobSchema()
        extracted_data = {}
        clt_id = request.headers['client_id']
        data = filter_fields_listing(data)
        audit_model = AuditTrailsSchema()
        service_name = request.url.path
        if not data.get('job_id'):
            extracted_data.update(
                {
                    "code": HTTP_204_NO_CONTENT,
                    "message": "Unable to perform operation, no information given",
                }
            )
            request.app.logger.debug(extracted_data)
            return extracted_data

        try:
            # data = {k: v for k, v in data.items() if len(v) >= 1}
            job_index_id = (
                get_job_index(data.get('job_id'))
            )
            if job_index_id:
                # Get the job details from job board
                job_board = JobBoardServices()
                job_details = job_board.check_job_exist(request, data.get('job_id'))
                request.app.logger.info("Response from Job Board '%s'", job_details)
                if job_details["code"] != HTTP_200_OK:
                    extracted_data.update(
                        {
                            "code": HTTP_400_BAD_REQUEST,
                            "message": "Unable to perform operation,"
                                       + "job reference id does not match with the given",
                        }
                    )
                    request.app.logger.debug(extracted_data)
                    return extracted_data

                request_data = {"index_id": job_index_id, "index_type": "Job"}
                # Job parsing block started
                # Search whether index id of type "job" for this
                # job document id is present in database
                index_matcher = MatchingIndexServices()
                job_index_exists = index_matcher.get_by_index_id_and_type(
                    request_data)
                request.app.logger.debug(
                    "Job index exists {}".format(job_index_exists))
                if job_index_exists is False:

                    # Add this job_document_id as a new
                    # index to Sovren of type "Job"
                    new_job_index = index_matcher.create_index(
                        request, job_index_id, "Job")
                    # logger.debug("New Job Index created '%s'", new_job_index)
                    invalid_strings = [
                        "MissingParameter",
                        "AuthenticationError",
                        "Unauthorized",
                    ]
                    if find_words_exists(invalid_strings,
                                         new_job_index["code"]):
                        extracted_data.update(
                            {
                                "code": HTTP_400_BAD_REQUEST,
                                "message": "Unable to perform operation, "
                                           + "unable to create new job index",
                            }
                        )
                        request.app.logger.debug(extracted_data)
                        return extracted_data
                # Call index a document to document the job
                # Add condition not to parse the job if
                # you already have job_details_id present
                job_parser = SovJobParserServices()
                if job_details.get("data").get("status-code") == HTTP_200_OK:
                    job_parser.parse_job(request, job_details,data.get('job_id'))
                    # Find the matching jobs
                    search_result = active_model.get_jobs(
                        data.get('job_id'), clt_id)
                    if search_result:
                        time_since_last_transaction = (
                                datetime.now() - search_result.created_at
                        )
                        if time_since_last_transaction.days > data.get('refresh_rate'):
                            del_trans = active_model.del_jobs(
                                data.get('job_id'), clt_id)
                            if del_trans:
                                matching_jobs = self.jobs_finder(
                                    job_index_id,
                                    data.get('job_id'),
                                    data.get('no_of_matches'),
                                    data.get('refresh_rate'),
                                    data
                                )
                                result = wrap_matching_jobs(matching_jobs.get('value'))
                                active_model.add_searched_result(
                                    data.get('job_id'),
                                    result,
                                    clt_id
                                )
                                request.app.logger.info("Result {}".format(result))
                                response = {}
                                response.update({
                                    'code': HTTP_200_OK,
                                    'data': result
                                })
                                audit_model.add(service_name,clt_id)
                                return response
                        else:
                            if len(search_result.srch_res) > 0:
                                if len(data) == common_url_settings.get("MATCHER_CHECK_LENGTH"):
                                    result = search_result.srch_res
                                else:
                                    matching_jobs = self.jobs_finder(
                                        job_index_id,
                                        data.get('job_id'),
                                        data.get('no_of_matches'),
                                        data.get('refresh_rate'),
                                        data
                                    )
                                    if matching_jobs.get('code') == HTTP_200_OK:
                                        result = wrap_matching_jobs(matching_jobs.get('value'))
                            else:
                                matching_jobs = self.jobs_finder(
                                    job_index_id,
                                    data.get('job_id'),
                                    data.get('no_of_matches'),
                                    data.get('refresh_rate'),
                                    data
                                )
                                if matching_jobs.get('code') == HTTP_200_OK:
                                    result = result = wrap_matching_jobs(matching_jobs.get('value'))
                                    if len(result) > 0:
                                        if len(data) == common_url_settings.get("MATCHER_CHECK_LENGTH"):
                                            active_model.add_searched_result(
                                                data.get('job_id'),
                                                result,
                                                clt_id
                                            )
                                else:
                                    return matching_jobs
                    else:
                        matching_jobs = self.jobs_finder(
                            job_index_id,
                            data.get('job_id'),
                            data.get('no_of_matches'),
                            data.get('refresh_rate'),
                            data
                        )
                        if matching_jobs.get('code') == HTTP_200_OK:
                            result = wrap_matching_jobs(matching_jobs.get('value'))
                            if len(result) > 0:
                                if len(data) == common_url_settings.get("MATCHER_CHECK_LENGTH"):
                                    active_model.add_searched_result(
                                        data.get('job_id'),
                                        result,
                                        clt_id
                                    )
                        else:
                            return matching_jobs
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
                else:
                    extracted_data.update({
                        "code": HTTP_400_BAD_REQUEST,
                        "message": "Job with given job id does not exists"
                    })
                    return extracted_data

            else:
                extracted_data.update(
                    {
                        "code": HTTP_400_BAD_REQUEST,
                        "message": "Unable to process the operation.",
                    }
                )
                request.app.logger.debug(extracted_data)
                return extracted_data
        except RequestException as e_msg:
            extracted_data.update(
                {
                    "code": HTTP_404_NOT_FOUND,
                    "message": "Unable to process the operation.",
                }
            )
            request.app.logger.error("Unable to process with {} exception".format(e_msg))
            return extracted_data

    def jobs_finder(self, index_id: str,
                    job_id: str,
                    no_of_matches: int,
                    refresh_rate: int,
                    data: dict) -> list:
        """
        Match's jobs with job and pull the result for client
        :param data: Dictionary
        :param refresh_rate: Integer
        :param no_of_matches: Integer
        :param job_id: String
        :param index_id: String
        :return: Dict
        """
        current_date = datetime.today().strftime("%Y-%m-%d")
        date_before_three_month = datetime.today() - timedelta(
            days=refresh_rate
        )
        payload = {
            "IndexIdsToSearchInto": [index_id],
            "Take": no_of_matches,
            "FilterCriteria": {
                "RevisionDateRange": {
                    "Minimum": date_before_three_month.strftime("%Y-%m-%d"),
                    "Maximum": current_date,
                },
            },
        }
        calling_api = (
                sovren_url_settings.get("SOVREN_MATCH_DOCUMENT_BY_ID_URL")
                + index_id
                + "/documents/"
                + job_id
        )
        payload = custom_all_filters(payload, data)
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
