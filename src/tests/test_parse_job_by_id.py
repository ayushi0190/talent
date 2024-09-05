# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Search jobs or resumes
@author <rchakraborty@simplifyvms.com>
"""
import json
import random
from faker import Faker
from src.tests.base_case import test_app
from src.tests.fake_client_registration import FakeClientRegistration
import logging
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY
from src.tests.test_helpers import TestHelpers
from src.utilities.custom_logging import CustomizeLogger

test_helper = TestHelpers()

logger = CustomizeLogger.make_logger()


class TestParseJobByIdParserServices:
    """
    Test TestParseJobByIdParserServices
    """

    def create_payload(self, job_id=None):
        """
        Create Payload
        :param param: String
        :return:
        """
        payload = {}
        if job_id:
            payload.update({
                "job_id": job_id
            })
        else:
            payload.update({
                "job_id": ""
            })
        return json.dumps(payload)

    def test_parse_job_by_id_successful_for_job_id(self, test_app):
        """
        Test successful for job id
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Parse Job By Id
        logger.info("************************************* Start of Parse Job by Id test case***************************************")
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_helper.parse_fake_job(authorization_response.get('client_id'), test_app)

        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            assert response_result.get("code") == HTTP_200_OK
            assert response_result.get("message") == "Successful transaction"
            logger.info("***********************************Pass Test Case for Parse Job By Id***************************")
            logger.info("Code we expect is 200, code we receive is:{}".format(response_result.get("code") ))

            latest_test_job = test_helper.get_last_parsed_job_id()
            delete_job = test_helper.delete_fake_job(authorization_response.get('client_id'),
                                                     latest_test_job,
                                                     test_app)
            assert delete_job.json().get("code") == HTTP_200_OK
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Fail Test Case for Parse Job By Id****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code ))

    def test_parse_job_by_id_fails_for_job_id(self, test_app):
        """
        Test failure for job id
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Parse Job By Id
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))

        response_register = test_app.post('/parse/job/by/id', headers=headers,
                                          data=self.create_payload())


        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("***********************************Parse Job By Id Fails For Absent Of Job Id****************************")
            logger.info("Code we expect is 200, code we receive is:",  response_register.status_code )

        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Parse Job By Id Fails For Absent Of Job Id****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code ))

        logger.info("************************************* End of Parse Job by Id test case***************************************")