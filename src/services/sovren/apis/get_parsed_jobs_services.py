# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Get Parsed Job Information
@author <sreddy@simplifyvms.com>
@author <satya@simplifyvms.com>
"""
import json
from typing import Dict
import requests
from requests.exceptions import RequestException
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.sovren.interfaces.searchers.get_parsed_jobs_interface import GetParsedJobsInterface
from src.services.sovren.helpers.misc_helpers import get_sovren_headers
from src.db.crud.sovren.prs_jobs_inf_schema import PrsJobInfSchema
from src.services.common.apis.job_board_services import JobBoardServices
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_404_NOT_FOUND
)
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema


class GetParsedJobsServices(GetParsedJobsInterface):
    """
    GetParsed Job services class
    """

    def get_parsed_job(self, request, job_document_id: str) -> Dict:
        """
        Get the detail of matching Job
        :param job_document_id:
        :return: Dict
        """
        if not job_document_id:
            extracted_data = {
                'code': HTTP_400_BAD_REQUEST,
                'message': 'Unable to perform operation, ' +
                           'no information given',

            }
            request.app.logger.debug(extracted_data)
            return extracted_data
        if job_document_id == '':
            extracted_data = {
                'code': HTTP_400_BAD_REQUEST,
                'message': 'Unable to perform operation, ' +
                           'job id not given'

            }
        else:
            job_board = JobBoardServices()
            job_details = job_board.check_job_exist(request, job_document_id)
            if job_details["code"] != HTTP_200_OK:
                extracted_data = {
                    "code": HTTP_400_BAD_REQUEST,
                    "message": "Unable to perform operation," + \
                        "job reference id does not match with the given",
                    }
                return extracted_data
            job_index_to_search = job_document_id.split("-")
            job_index = job_index_to_search[0] + '-' + job_index_to_search[1] + '-' + \
                           job_index_to_search[2] + '-' + job_index_to_search[3]
            calling_api = sovren_url_settings.get(
                "SOVREN_CREATE_INDEX_URL") + job_index + '/documents/' + job_document_id
            return self.connect_to_api(request, get_sovren_headers(), calling_api, job_document_id)
        request.app.logger.debug(extracted_data)
        return extracted_data
    def connect_to_api(self, request, header: dict, calling_api: str, job_document_id: str) -> dict:
        """
        Connect to Sovren and find resume details
        :param job_id: String
        :param job_index: String
        :param header:  Dictionary
        :param calling_api: String
        :return:
        """
        clt_id = request.headers['client_id']
        audit_model = AuditTrailsSchema()
        service_name = request.url.path
        result = {}
        try:
            job_info = PrsJobInfSchema()
            get_job = job_info.get(job_document_id)
            if get_job:
                response_info = json.loads(get_job.job_res)
                response_info.get('Value').pop('CreditsRemaining')
                result.update({
                    'code': HTTP_200_OK,
                    'value': response_info.get('Value')
                })
                audit_model.add(service_name,clt_id)
            else:
                response = requests.request("GET", url=calling_api, headers=header)
                response_info = json.loads(json.dumps(response.json()))
                if response.status_code == HTTP_200_OK:
                    result.update({
                        'code': HTTP_200_OK,
                        'value': response_info.get("Value")
                    })
                    audit_model.add(service_name,clt_id)
                else:
                    result.update({
                        'code': HTTP_404_NOT_FOUND,
                        'value': response_info.get("Info").get('Message')
                    })
            request.app.logger.debug(result)
            return result
        except RequestException as e_msg:
            extracted_data = {
                'code': HTTP_422_UNPROCESSABLE_ENTITY,
                'value': None
            }
            request.app.logger.error("Unable to perform Operation with {} exception".format(e_msg))
            return extracted_data
