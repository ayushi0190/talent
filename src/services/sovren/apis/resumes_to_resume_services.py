# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Get matching Resumes for a given Resume from sovren services
@author <sreddy@simplifyvms.com>
"""
import json
from datetime import datetime, timedelta
from typing import Any, Dict, List, Union

import requests
from requests.exceptions import RequestException
from starlette.status import (HTTP_200_OK, HTTP_204_NO_CONTENT,
                              HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)

from src.db.crud.sovren.resumes_to_resume_schema import ResumesToResumeSchema
from src.services.common.config.common_config import common_url_settings
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.sovren.helpers.resumes_to_resume_helpers import wrap_matching_resumes
from src.services.sovren.helpers.misc_helpers import (get_sovren_headers,
                                                      filter_fields_listing,
                                                      data_with_no_of_matches,
                                                      get_resume_index)
from src.services.sovren.helpers.search_job_resume_helpers import custom_all_filters
from src.services.sovren.interfaces.matchers.resumes_to_resume_interface import \
    IResumesToResume
from src.services.common.helpers.misc_helpers import get_authorized_services
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema

class ResumesToResumeServices(IResumesToResume):
    """
    Resumes To Resume class
    """

    def get_matched_resumes(
            self, request, data: dict) -> List[Dict[str, Union[str, Any]]]:
        """
        Get list of Resumes matching to resumes
        :param data: Dictionary
        :return: Dict
        """
        active_model = ResumesToResumeSchema()
        extracted_data = {}
        clt_id = request.headers['client_id']
        data = filter_fields_listing(data)
        audit_model = AuditTrailsSchema()
        service_name = request.url.path
        if not data.get("resume_id"):
            extracted_data.update(
                {
                    "code": HTTP_204_NO_CONTENT,
                    "message": "Unable to perform operation, no information given",
                }
            )
            request.app.logger.debug(extracted_data)
            return extracted_data

        try:
            if common_url_settings.get("INTERNAL_BUCKET"):
                # Find the matching resumes
                search_result = active_model.get_resumes(
                    data.get("resume_id"), clt_id)
                if search_result:
                    time_since_last_transaction = (
                        datetime.now() - search_result.created_at
                    )
                    if time_since_last_transaction.days > data.get('refresh_rate'):
                        del_trans = active_model.del_jobs(
                            data.get("resume_id"), clt_id)
                        if del_trans:
                            matching_resumes = self.resumes_finder(request, data.get("resume_id"), data)
                            if matching_resumes.get('code') == HTTP_200_OK:
                                result = wrap_matching_resumes(matching_resumes.get('value'), data)
                                if len(result) > 0:
                                    if len(data) == common_url_settings.get("MATCHER_CHECK_LENGTH"):
                                        active_model.add_searched_result(
                                            data.get("resume_id"), result, clt_id
                                        )
                            else:
                                return matching_resumes

                    else:
                        if len(search_result.srch_res) > 0:
                            if len(data) == common_url_settings.get("MATCHER_CHECK_LENGTH"):
                                result = search_result.srch_res
                            else:
                                matching_resumes = self.resumes_finder(request, data.get("resume_id"), data)
                                if matching_resumes.get('code') == HTTP_200_OK:
                                    result = wrap_matching_resumes(matching_resumes.get('value'), data)
                        else:
                            matching_resumes = self.resumes_finder(request, data.get("resume_id"), data)
                            if matching_resumes.get('code') == HTTP_200_OK:
                                result = wrap_matching_resumes(matching_resumes.get('value'), data)
                                if len(result) > 0:
                                    if len(data) == common_url_settings.get("MATCHER_CHECK_LENGTH"):
                                        active_model.add_searched_result(
                                            data.get("resume_id"), result, clt_id
                                        )
                            else:
                                return matching_resumes

                else:
                    matching_resumes = self.resumes_finder(request, data.get("resume_id"), data)
                    if matching_resumes.get('code') == HTTP_200_OK:
                        result = wrap_matching_resumes(matching_resumes.get('value'), data)
                        if len(result) > 0:
                            if len(data) == common_url_settings.get("MATCHER_CHECK_LENGTH"):
                                active_model.add_searched_result(
                                    data.get("resume_id"), result, clt_id
                                )
                    else:
                        return matching_resumes

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
            extracted_data.update(
                {
                    "code": HTTP_404_NOT_FOUND,
                    "message": "Unable to process the operation.",
                }
            )
            request.app.logger.error("Unable to perform operation with {}".format(e_msg))
            return extracted_data

    def resumes_finder(self, request, resume_id: str, data: dict) -> list:
        """
        Match's resumes with resume and pull the result for client
        :param resume_id: String
        :return: Dict
        """
        current_date = datetime.today().strftime('%Y-%m-%d')
        date_before_three_month = datetime.today() - timedelta(
            days=int(data.get('refresh_rate')))
        index_id = get_resume_index(resume_id)
        resume_index = []
        service_info = get_authorized_services(request)
        if service_info:
            if service_info.pol_shr and service_info.pol_prv:
                resume_index_id = common_url_settings.get("INTERNAL_BUCKET")
                resume_index.append(resume_index_id)
                resume_index.append(service_info.clt_res_idx_id)
                if resume_index_id not in ('simp-r-ex-intern','SIMP-R-EX-INTERN'):
                    resume_index_id = service_info.clt_res_idx_id
            elif service_info.pol_shr:
                resume_index_id = common_url_settings.get("INTERNAL_BUCKET")
                resume_index.append(resume_index_id)
            elif service_info.pol_prv:
                resume_index.append(service_info.clt_res_idx_id)
                resume_index_id = service_info.clt_res_idx_id
        else:
            if resume_index_id in ('simp-r-ex-intern','SIMP-R-EX-INTERN'):
                resume_index_id = common_url_settings.get("INTERNAL_BUCKET")
                resume_index.append(resume_index_id)
            else:
                resume_index.append(resume_index_id)
        payload = {
            "IndexIdsToSearchInto": resume_index,
            "Take" : data.get('no_of_matches'),
            "FilterCriteria": {
                "RevisionDateRange": {
                    "Minimum": date_before_three_month.strftime("%Y-%m-%d"),
                    "Maximum": current_date,
                },
            },
        }
        request.app.logger.info("Sovren Payload {}".format(payload))
        calling_api = (
            sovren_url_settings.get("SOVREN_MATCH_DOCUMENT_BY_ID_URL")
            + index_id
            + "/documents/"
            + resume_id
        )
        payload = custom_all_filters(payload, data)
        response = self.connect_to_resumes_finder_api(
            request, get_sovren_headers(), payload, calling_api
        )
        if not response:
            response.append({"code": HTTP_400_BAD_REQUEST})
        return response

    def connect_to_resumes_finder_api(
        self, request, header: dict, payload: dict, calling_api: str
    ) -> list:
        """
        Connect to Sovren and find similar Resumes to a given Resume
        :param header:  Dictionary
        :param payload: Dictionary
        :param calling_api: String
        :return:
        """
        try:
            response = requests.request(
                "POST", url=calling_api, data=json.dumps(payload), headers=header
            )
            request.app.logger.info("Sovren Response {}".format(response))
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
