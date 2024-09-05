# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Get candidate resume
@author <rchakraborty@simplifyvms.com>
"""
import json
import logging
from faker import Faker
from src.tests.base_case import test_app
from src.tests.fake_client_registration import FakeClientRegistration
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY, \
    HTTP_304_NOT_MODIFIED
from src.tests.test_helpers import TestHelpers
from src.utilities.custom_logging import CustomizeLogger

test_helper = TestHelpers()

logger = CustomizeLogger.make_logger()


class TestSearchParsedResume:
    """
    Test TestSearchParsedResume
    """
    def create_payload(self, resume_id=''):
        """
        Create Payload
        :param resume_id: String
        :return:
        """
        payload = {}
        if resume_id:
            payload.update({
                "resume_id": resume_id
            })
        else:
            payload.update({
                "resume_id": ""
            })
        return json.dumps(payload)

    def test_successful_search_parsed_resume_service(self, test_app):
        """
        Test successful Search Parsed Resume services
        :param test_app:
        :return:
        """
        logger.info("************************************* Start of Search Parsed Resume test case***************************************")
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = {
            "Content-Type": "application/json",
            "client_id": authorization_response.get('client_id')
        }
        resume_response = test_helper.parse_fake_resume(authorization_response.get('client_id'),
                                                        test_app)
        response_result = resume_response.json()
        if response_result.get("code") == HTTP_200_OK or response_result.get("code") == HTTP_304_NOT_MODIFIED:
            latest_test_resume = test_helper.get_last_parsed_resume_id()
            candidate_resume = test_app.post('/search/parsed/resume', headers=headers,
                                             data=self.create_payload(latest_test_resume))
            if candidate_resume.status_code == HTTP_200_OK:
                # Try to assert the token value received
                response_result = candidate_resume.json()
                if response_result.get("code") == HTTP_200_OK or \
                response_result.get("code") == HTTP_204_NO_CONTENT:
                    assert response_result.get("code") == HTTP_200_OK or \
                        response_result.get("code") == HTTP_204_NO_CONTENT

                logger.info("***********************************Pass test case for Search Parsed Resume****************************")
                logger.info("Code we expect is 200 or 204, code we receive is:{}".format(candidate_resume.status_code))

                delete_resume = test_helper.delete_fake_resume(authorization_response.get('client_id'),
                                                               latest_test_resume, test_app)

                assert delete_resume.status_code == HTTP_200_OK
        else:
            assert response_result.get("code") == HTTP_404_NOT_FOUND
            logger.info("***********************************Pass test case for Search Parsed Resume****************************")
            logger.info("Code we expect is 404, code we receive is:{}".format(response_result.get("code")))

    def test_unsuccessful_search_parsed_resume_service(self, test_app):
        """
        Test unsuccessful search parsed resume services
        :param test_app:
        :return:
        """
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = {
            "Content-Type": "application/json",
            "client_id": authorization_response.get('client_id')
        }
        candidate_resume = test_app.post('/search/parsed/resume', headers=headers,
                                         data=self.create_payload())
        if candidate_resume.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = candidate_resume.json()
            assert response_result.get("code") == HTTP_422_UNPROCESSABLE_ENTITY

            logger.info("***********************************Get Search Parsed Resume Fails For Absent of Resume Id****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(candidate_resume.status_code))

        else:
            assert candidate_resume.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Get Search Parsed Resume Fails For Absent of Resume Id****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(candidate_resume.status_code))

    def test_unsuccessful_search_parsed_resume_for_false_res_id(self, test_app):
        """
        Test unsuccessful search parsed resume services
        :param test_app:
        :return:
        """
        fake = Faker()
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = {
            "Content-Type": "application/json",
            "client_id": authorization_response.get('client_id')
        }
        fake_resume_id = "{}-R-{}-{}-{}-{}".format(fake.pystr(),
                                                   fake.random_int(1500000000, 1583916379),
                                                   fake.pystr(),
                                                   fake.pystr(),
                                                   fake.random_int())
        candidate_resume = test_app.post('/search/parsed/resume', headers=headers,
                                         data=self.create_payload(fake_resume_id))
        if candidate_resume.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = candidate_resume.json()
            if int(response_result.get('code')) == HTTP_404_NOT_FOUND:
                assert response_result.get("code") == HTTP_404_NOT_FOUND
            logger.info("***********************************Get Searched Parsed Resume Fails For Wrong Resume Id****************************")
            logger.info("Code we expect is 404, code we receive is:{}".format(response_result.get('code')))

        else:
            assert candidate_resume.status_code == HTTP_404_NOT_FOUND
            logger.info("***********************************Get Search Parsed Resume Fails For Wrong Resume Id****************************")
            logger.info("Code we expect is 404, code we receive is:{}".format(candidate_resume.status_code))

        logger.info("************************************* End of Search Parsed Resume test case***************************************")