# -*- coding: utf-8 -*-
import json
import requests
from starlette import status

from src.utilities.custom_logging import cust_logger as logger

def connect_to_api(header: dict, payload: dict, api_url: str,
                   api_name: str, msg_dict: dict = {}) -> dict:
    """
    Connect to API
    :param : header
    :param : payload
    :param : calling_api
    :return:
    """
    result = {}
    try:
        msg_success = msg_dict.get('success', 'API call successful: ' + api_name)
        msg_fail = msg_dict.get('fail', 'API call failed: ' + api_name)
        msg_error = msg_dict.get('error', 'Error in API call: ' + api_name)
        response = requests.request(
            "POST", headers=header, data=json.dumps(payload), url=api_url
        )
        response_info = response.json()

        if response.status_code == status.HTTP_200_OK:
            logger.info(msg_success)
            return response_info
        else:
            result = {"code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                      "message": msg_fail
                      }
            logger.error(msg_fail)
        return result
    except Exception as ex:
        err_msg = "{} with error: {}".format(msg_error, str(ex))
        logger.error(err_msg)
        result.update({
            "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": err_msg,
            "error": "Exception is :" + str(ex)
        })
        return result
