# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Job board related services
@author <rchakraborty@simplifyvms.com>
"""
import json

import requests
from requests.exceptions import RequestException
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_500_INTERNAL_SERVER_ERROR

from src.services.common.config.common_config import common_url_settings
from src.services.common.interfaces.job_board_interface import IJobBoard
from src.utilities.custom_logging import cust_logger as logger


class JobBoardServices(IJobBoard):
    """
    Job board services
    """

    def check_job_exist(self, request, job_id: str) -> dict:
        """
        Get the result from Job Board
        :param : request
        :param : job_id
        :return
        """
        header = {
            "Content-Type": "application/json",
            "Accept":"application/json",
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Authorization": common_url_settings.get("JOB_BOARD_AUTHORIZATION")
            }
        payload = {"job_reference_number": job_id}
        result = self.connect_to_job_board_api(request, header, payload, common_url_settings.get(
                "JOB_BOARD_JOB_DETAILS_URL")
        )
        return result

    def connect_to_job_board_api(self, request, header: dict, payload: dict,
                                 calling_api: str) -> dict:
        """
        Connect to Job Board API to check whether Job exist or NOT
        :param : request
        :param : header
        :param : payload
        :param : calling_api
        :return:
        """
        result = {}
        try:
            response = requests.post(calling_api, headers=header, json=payload)
            response_info = response.json()
            print(response_info)
            if response.status_code == HTTP_200_OK:
                result = {
                    "code": HTTP_200_OK,
                    "message": "Job exist on JOB Board",
                    "data": response_info,
                }
                logger.info("Job exist on JOB Board")
            else:
                result = {"code": HTTP_204_NO_CONTENT,
                          "message": "Job does not exist on JOB Board"
                          }
                logger.error("Job does not exist on JOB Board")
            return result
        except Exception as ex:
            logger.error("Error while getting details from JOB Board %s " % str(ex))
            result.update({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error while getting details from JOB Board ",
                "error": "Exception is :" + str(ex)
            })
            return result