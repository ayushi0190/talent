from typing import Optional, List

from pydantic import BaseModel, validator
import docx2txt
import json
from universities import API
from faker import Faker
from src.tests.fake_client_registration import FakeClientRegistration
from src.tests.test_helpers import TestHelpers
from src.tests.base_case import test_app
import logging
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST
from src.utilities.custom_logging import CustomizeLogger

test_helper = TestHelpers()

logger = CustomizeLogger.make_logger()


class TestParseJobByDescriptionParserServices:
    """
    Test parse job by description
    """

    def create_payload(self, param=''):
        """
        Create Payload
        :param param: String
        :return:
        """
        fake = Faker()
        job_tittle = fake.pystr()
        job_description = fake.pystr()
        client_name = fake.pystr()
        country = fake.pystr()
        city = fake.pystr()
        state = fake.pystr()
        zip = fake.pystr()

        return json.dumps({
            "job_title": job_tittle,
            "job_description": job_description,
            "client_name": client_name,
            "work_location": [
                {
                    "country": country,
                    "city": city,
                    "state": state,
                    "zip": zip
                }
            ]
        })

    def test_parse_job_by_description_successful_for_job_description(self, test_app):
        """
        Test successful for job description
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first
        logger.info("************************************* Start of Parse Job by Description test case***************************************")
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        response = test_helper.parse_fake_job_by_description(authorization_response.get('client_id'),
                                                             test_app)

        if response.status_code == HTTP_200_OK:
            response_result = response.json()
            if response_result.get("code") == HTTP_200_OK:
                assert response_result.get("code") == HTTP_200_OK
                assert response_result.get("message") == "Successful transaction"
                logger.info("***********************************Pass Test Case for Parse Job By Description****************************")
                logger.info("Code we expect is 200, code we receive is:{}".format(response_result.get("code") ))

                latest_test_job = test_helper.get_last_parsed_job_id()
                delete_job = test_helper.delete_fake_job(authorization_response.get('client_id'),
                                                        latest_test_job,
                                                        test_app)
                assert delete_job.json().get("code") == HTTP_200_OK
            else:
                assert response_result.get("code") == HTTP_400_BAD_REQUEST
                logger.info("***********************************Fail test case for Parse Job By Description****************************")
                logger.info("Code we expect is 400, code we receive is:{}".format(response_result.get("code") ))

        else:
            assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Fail Test Case for Parse Job By Description****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response.status_code ))

    def test_parse_job_by_description_fails_for_job_title(self, test_app):
        """
        Test failure for job tittle
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Parse Job By Description
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))

        response_register = test_app.post('/parse/job/by/description', headers=headers,
                                          data=self.create_payload('job_tittle'))

        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("***********************************Parse Job By Description Fails For Absent Of Job Tittle****************************")
            logger.info("Code we expect is 400, code we receive is:{}".format(response_result.get("code")) )

        else:
            assert response_register.status_code == HTTP_500_INTERNAL_SERVER_ERROR
            logger.info("***********************************Parse Job By Description Fails For Absent Of Job Tittle****************************")
            logger.info("Code we expect is 500, code we receive is:{}".format(response_register.status_code) )

    def test_parse_job_by_description_fails_for_job_description(self, test_app):
        """
        Test failure for job description
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Parse Job By Description
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))

        response_register = test_app.post('/parse/job/by/description', headers=headers,
                                          data=self.create_payload('job_description'))

        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("***********************************Parse Job By Description Fails For Absent Of Job Description****************************")
            logger.info("Code we expect is 400, code we receive is:{}".format(response_result.get("code")) )

        else:
            assert response_register.status_code == HTTP_500_INTERNAL_SERVER_ERROR
            logger.info("***********************************Parse Job By Description Fails For Absent Of Job Description****************************")
            logger.info("Code we expect is 500, code we receive is:{}".format(response_register.status_code) )

    def test_parse_job_by_description_fails_for_client_name(self, test_app):
        """
        Test failure for client name
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Parse Job By Description
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))

        response_register = test_app.post('/parse/job/by/description', headers=headers,
                                          data=self.create_payload('client_name'))

        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("***********************************Parse Job By Description Fails For Absent Of Client Name****************************")
            logger.info("Code we expect is 400, code we receive is:{}".format(response_result.get("code")) )

        else:
            assert response_register.status_code == HTTP_500_INTERNAL_SERVER_ERROR
            logger.info("***********************************Parse Job By Description Fails For Absent Of Client Name****************************")
            logger.info("Code we expect is 500, code we receive is:{}".format(response_register.status_code) )

    def test_parse_job_by_description_fails_for_work_location(self, test_app):
        """
        Test failure for work location
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Parse Job By Description
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))

        response_register = test_app.post('/parse/job/by/description', headers=headers,
                                          data=self.create_payload('work_location'))

        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("***********************************Parse Job By Description Fails For Absent Of Work Location****************************")
            logger.info("Code we expect is 400, code we receive is:{}".format(response_result.get("code")) )

        else:
            assert response_register.status_code == HTTP_500_INTERNAL_SERVER_ERROR
            logger.info("***********************************Parse Job By Description Fails For Absent Of Work Location****************************")
            logger.info("Code we expect is 500, code we receive is:{}".format(response_register.status_code) )

    def test_parse_job_by_description_fails_for_country(self, test_app):
        """
        Test failure for Country
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Parse Job By Description
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))

        response_register = test_app.post('/parse/job/by/description', headers=headers,
                                          data=self.create_payload('country'))

        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("***********************************Parse Job By Description Fails For Absent Of Country****************************")
            logger.info("Code we expect is 400, code we receive is:{}".format(response_result.get("code")) )

        else:
            assert response_register.status_code == HTTP_500_INTERNAL_SERVER_ERROR
            logger.info("***********************************Parse Job By Description Fails For Absent Of Country****************************")
            logger.info("Code we expect is 500, code we receive is:{}".format(response_register.status_code) )

    def test_parse_job_by_description_fails_for_city(self, test_app):
        """
        Test failure for City
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Parse Job By Description
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))

        response_register = test_app.post('/parse/job/by/description', headers=headers,
                                          data=self.create_payload('city'))

        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("***********************************Parse Job By Description Fails For Absent Of City****************************")
            logger.info("Code we expect is 400, code we receive is:{}".format(response_result.get("code")) )

        else:
            assert response_register.status_code == HTTP_500_INTERNAL_SERVER_ERROR
            logger.info("***********************************Parse Job By Description Fails For Absent Of City****************************")
            logger.info("Code we expect is 500, code we receive is:{}".format(response_register.status_code ))

    def test_parse_job_by_description_fails_for_state(self, test_app):
        """
        Test failure for State
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Parse Job By Description
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))

        response_register = test_app.post('/parse/job/by/description', headers=headers,
                                          data=self.create_payload('state'))

        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("***********************************Parse Job By Description Fails For Absent Of State****************************")
            logger.info("Code we expect is 400, code we receive is:{}".format(response_result.get("code")) )

        else:
            assert response_register.status_code == HTTP_500_INTERNAL_SERVER_ERROR
            logger.info("***********************************Parse Job By Description Fails For Absent Of State****************************")
            logger.info("Code we expect is 500, code we receive is:{}".format(response_register.status_code ))

    def test_parse_job_by_description_fails_for_zip(self, test_app):
        """
        Test failure for Zip
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Parse Job By Description
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))

        response_register = test_app.post('/parse/job/by/description', headers=headers,
                                          data=self.create_payload('zip'))

        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("***********************************Parse Job By Description Fails For Absent Of Zip****************************")
            logger.info("Code we expect is 400, code we receive is:{}".format(response_result.get("code")) )

        else:
            assert response_register.status_code == HTTP_500_INTERNAL_SERVER_ERROR
            logger.info("***********************************Parse Job By Description Fails For Absent Of Zip****************************")
            logger.info("Code we expect is 500, code we receive is:{}".format(response_register.status_code ))

        logger.info("************************************* End of Parse Job by Description test case***************************************")