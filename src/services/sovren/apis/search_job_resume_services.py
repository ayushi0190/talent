# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Searcher Jobs and Resumes from sovren service
@author <sreddy@simplifyvms.com>
@author <satya@simplifyvms.com>
"""
import json
from typing import Dict

import requests
from requests.exceptions import RequestException
from starlette.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST,
                              HTTP_422_UNPROCESSABLE_ENTITY)

from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.sovren.helpers.misc_helpers import get_sovren_headers
from src.services.sovren.interfaces.searchers.search_job_resume_interface import \
    SearchJobResumeInterface
from src.services.common.apis.matching_index_services import \
    MatchingIndexServices

from src.services.sovren.helpers.search_job_resume_helpers import search_job_resume_data, custom_all_filters
from src.db.crud.common.matching_index_schema import MatchingIndexSchema

class SearchJobResumeServices(SearchJobResumeInterface):
    """
    Job to jobs services class
    """

    def get_search_jobs_resumes(self, request, data: dict) -> Dict:
        """
        Get the detail of matching resume
        :param data:
        :param request:
        :return: Dict
        """
        if not data:
            extracted_data = {
                'code': HTTP_400_BAD_REQUEST,
                'message': 'Unable to perform operation, ' +
                           'no information given',

            }
            request.app.logger.debug(extracted_data)
            return extracted_data
        else:
            try:
                mat_index_schema = MatchingIndexSchema()
                if data.get('Titles') is None or len(data.get('Titles')) == 0:
                    extracted_data = {
                        'code': HTTP_400_BAD_REQUEST,
                        'message': 'Unable to perform operation, No Titles given',

                    }
                    request.app.logger.debug(extracted_data)
                    return extracted_data
                elif data.get('Skills') is None or len(data.get('Skills')) == 0:
                    extracted_data = {
                        'code': HTTP_400_BAD_REQUEST,
                        'message': 'Unable to perform operation, no Skills given',

                    }
                    request.app.logger.debug(extracted_data)
                    return extracted_data

                elif data.get('BucketType') is None or len(data.get('BucketType')) == 0:
                    extracted_data = {
                        'code': HTTP_400_BAD_REQUEST,
                        'message': 'Unable to perform operation, no BucketType given',

                    }
                    request.app.logger.debug(extracted_data)
                    return extracted_data


                if data.get('BucketId') is None or len(data.get('BucketId')) == 0:
                    request_data = {
                        "index_type": data.get('BucketType')
                    }
                    index_matcher = MatchingIndexServices()
                    list_index = index_matcher.get_by_index_id_and_index_type(request_data)
                    list_index = [j.idx_id for j in list_index]
                else:
                    list_index = data.get('BucketId')
                if not(data.get('bucket_source') is None or len(data.get('bucket_source')) == 0):
                    if data.get('bucket_source')[0] == 'All':
                        request_data = {
                            "index_type": data.get('BucketType')
                        }
                        index_matcher = MatchingIndexServices()
                        list_index = index_matcher.get_by_index_id_and_index_type(request_data)
                        list_index = [j.idx_id for j in list_index]
                    else:
                        list_index = mat_index_schema.get_index_id_by_bucket_source_name(data.get("bucket_source"))
                if data.get('Count') is None or data.get('Count') == 0:
                    count = 20
                else:
                    count = data.get('Count')
                payload = {'IndexIdsToSearchInto': list_index,
                           'PaginationSettings': {'Take': 100}, 'FilterCriteria': {}}
                if data.get('AppliedJobs') is not None \
                        and len(data.get('AppliedJobs')) > 0:
                    applied_jobs = [ids.lower() for ids in data.get('AppliedJobs')]
                else:
                    applied_jobs = []
                payload = custom_all_filters(payload, data)
                payload.get('FilterCriteria').pop('JobTitles')
                calling_api = sovren_url_settings.get("SOVREN_SEARCH_URL")
                return self.connect_to_api(request, get_sovren_headers(), calling_api, payload, applied_jobs, \
                                           data.get('BucketType'), count)
            except ValueError:
                extracted_data = {}
                extracted_data.update({
                    'code': HTTP_400_BAD_REQUEST,
                    'message': 'Unable to process the operation.'
                })
                request.app.logger.error(extracted_data)
                return extracted_data

    def connect_to_api(self, request, header: dict, calling_api: str, payload: dict, applied_jobs: list, \
                       buckettype: str, count: int) -> dict:
        """
        Connect to Sovren and find resume details
        :param resume_id: String
        :param resume_index: String
        :param header:  Dictionary
        :param calling_api: String
        :return:
        """

        data = json.dumps(payload, indent=4, sort_keys=True, default=str)
        request.app.logger.debug("Search Operation Payload {}".format(data))
        response = requests.request("POST", url=calling_api, headers=header, data=data)
        try:
            bucket_type = buckettype
            response_info = json.loads(json.dumps(response.json()))
            if response.status_code == HTTP_200_OK:
                return search_job_resume_data(request, response_info, bucket_type, applied_jobs, count)
            else:
                extracted_data = {
                    'code': response.status_code,
                    'message': response_info.get("Info").get('Message')
                }
                request.app.logger.debug('Error Because of {}'.format(response))
                return extracted_data
        except RequestException as e_msg:
            extracted_data = {
                'code': HTTP_422_UNPROCESSABLE_ENTITY,
                'value': None
            }
            request.app.logger.error("Unable to perform operation with {}".format(e_msg))
            return extracted_data
