# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Matching index services
@author <rchakraborty@simplifyvms.com>
"""

import json
from abc import ABC

import requests
from requests.exceptions import RequestException
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_409_CONFLICT

from src.db.crud.common.matching_index_schema import MatchingIndexSchema
from src.services.common.interfaces.matching_index_interface import \
    IMatchingIndex
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.sovren.helpers.misc_helpers import get_sovren_headers
from src.utilities.custom_logging import cust_logger as logger


class MatchingIndexServices(IMatchingIndex, ABC):
    """
    Job board services
    """
    def get_by_index_id_and_type(self, data: dict) -> dict:
        """
        Get the result Matching Index collection
        :param data: Dictionary
        :return:
        """
        model = MatchingIndexSchema()
        return model.check_index(data)

    def create_index(self, request, index_id: str, index_type: str) -> dict:
        """
        Create Index from Sovren and Save to DB
        :param index_id: String
        :param index_type: String
        :return:
        """
        result = {}
        model = MatchingIndexSchema()
        payload = {"IndexType": index_type}
        calling_api = sovren_url_settings.get(
            "SOVREN_CREATE_INDEX_URL") + index_id
        result = self.connect_to_api(request,
                                     get_sovren_headers(), payload, calling_api)

        if result.get("code") not in [HTTP_200_OK,HTTP_409_CONFLICT]:
            return result

        # Save response to DB
        data = {}
        data.update({
            "idx_id": index_id,
            "idx_tpe": index_type,

        })

        if result.get("code") in [HTTP_200_OK,HTTP_409_CONFLICT]:
            logger.info("Save in DB ")
            model.create_record(request,index_id, index_type)
            return result

    def connect_to_api(self, request, header: dict, payload: dict,
                       calling_api: str) -> dict:
        """
        Call Sovren API to create Index
        :param header: Dictionary
        :param payload: Dictionary
        :param calling_api: String
        :return: JSON
        """
        result = {}
        try:
            response = requests.request("POST", headers=header, \
                                        data=json.dumps(payload), url=calling_api)
            logger.info("Sovren response for Index creation %s " % response)
            if response.status_code == HTTP_200_OK:
                response_info = json.loads(json.dumps(response.json()))
                result = {"code": HTTP_200_OK, \
                          'message': "Index created successfully from Sovren", \
                          "data": response_info}

                logger.info("Index created successfully from Sovren %s " % response.reason)
            else:
                result = {"code": response.status_code, \
                          "message": response.reason, \
                          "error": "Sovren unable to create Index"}
                logger.info("Sovren unable to create Index ")
            return result

        except Exception as ex:
            logger.info("Error in creating Index from Sovren %s " % str(ex))
            result.update({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error in creating Index from Sovren ",
                "error": "Exception is :" + str(ex)
            })
            return result

    def get_by_index_id_and_index_type(self, data: dict) -> dict:
        """
        Get the result Matching Index collection
        :param data: Dictionary
        :return:
        """
        model = MatchingIndexSchema()
        return model.get_list(data)
