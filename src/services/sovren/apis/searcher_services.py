# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Searcher services
@author <rchakraborty@simplifyvms.com>
"""
import json
from abc import ABC
from typing import Dict

import requests
from starlette.status import (HTTP_200_OK, HTTP_204_NO_CONTENT,
                              HTTP_400_BAD_REQUEST,
                              HTTP_422_UNPROCESSABLE_ENTITY)

from src.services.common.config.common_config import common_url_settings
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.sovren.helpers.misc_helpers import get_sovren_headers
from src.services.common.helpers.misc_helpers import find_words_exists
from src.services.sovren.interfaces.searchers.searcher_interface import \
    SearcherInterface

from src.db.crud.sovren.mp_tp_res_schema import MpTpResSchema
from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from src.db.crud.sovren.intern_res_schema import InternResSchema
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema

class SovrenSearcherServices(SearcherInterface, ABC):
    """
    Job to jobs services class
    """

    def get_parsed_resume(self, request: str, resume_id: str) -> Dict:
        """
        Get the detail of matching resume
        :param resume_id:
        :return: Dict
        """
        if not resume_id:
            extracted_data = {
                'code': HTTP_400_BAD_REQUEST,
                'message': 'Unable to perform operation, ' +
                           'no information given',

            }
            return extracted_data
        if resume_id == '':
            extracted_data = {
                'code': HTTP_400_BAD_REQUEST,
                'message': 'Unable to perform operation, ' +
                           'resume id not given'

            }
            return extracted_data
        resume_index_to_search = resume_id.split("-")
        resume_index = resume_index_to_search[0] + '-' + resume_index_to_search[1] + '-' + \
            resume_index_to_search[3] + '-' + resume_index_to_search[4]
        resume_indexes = ["simp-r-ex-intern", "SIMP-R-EX-INTERN",
                          "SIMP-R-CAREER-X", "SIMP-R-SVMS-X"]
        if find_words_exists(resume_indexes, resume_index):
            resume_index = common_url_settings.get(
                "INTERNAL_BUCKET")
        calling_api = sovren_url_settings.get(
            "SOVREN_CREATE_INDEX_URL") + resume_index + '/documents/' + resume_id
        return self.connect_to_api(
            request, get_sovren_headers(), calling_api, resume_index, resume_id)

    def connect_to_api(self, request: str, header: dict, calling_api: str,
                       resume_index: str, resume_id: str = "") -> dict:
        """
        Connect to Sovren and find resume details
        :param resume_id: String
        :param resume_index: String
        :param header:  Dictionary
        :param calling_api: String
        :return:
        """
        clt_id = request.headers['client_id']
        audit_model = AuditTrailsSchema()
        service_name = request.url.path
        result = {}
        response = requests.request("GET", url=calling_api, headers=header)
        try:
            if response.status_code == HTTP_200_OK:
                response_info = json.loads(json.dumps(response.json()))
                if response_info["Info"].get("Code") == "Success":
                    prs_res_info = PrsResInfSchema()
                    get_contact = prs_res_info.get(resume_id)
                    if not get_contact:
                        intern_resume = InternResSchema()
                        get_contact = intern_resume.get(resume_id)
                        if get_contact:
                            data = json.loads(get_contact.resp)
                            data = json.loads(data['Value']['ParsedDocument'])
                            get_contact = data['Resume']['StructuredXMLResume'].get('ContactInfo')
                            if not get_contact:
                                result.update({
                                    'ContactInfo': None
                                })
                            else:
                                result.update({
                                    'ContactInfo': get_contact
                                })
                        else:
                            result.update({
                                'ContactInfo': None
                            })
                    else:
                        data = json.loads(get_contact.resp)
                        data = json.loads(data['Value']['ParsedDocument'])
                        get_contact = data['Resume']['StructuredXMLResume'].get('ContactInfo')
                        if not get_contact:
                            result.update({
                                'ContactInfo': None
                            })
                        else:
                            result.update({
                                'ContactInfo': get_contact
                            })
                    result.update({
                        'code': HTTP_200_OK,
                        'value': response_info["Value"]
                    })
                else:
                    result.update({
                        'code': HTTP_204_NO_CONTENT,
                        'value': response_info["Value"]
                    })
                audit_model.add(service_name,clt_id)
            else:
                result.update({
                    'code': response.status_code,
                    'value': response.json()['Info']['Message']
                })
            return result
        # pylint: disable=W0703
        except Exception:
            extracted_data = {
                'code': HTTP_422_UNPROCESSABLE_ENTITY,
                'value': None
            }
            return extracted_data
