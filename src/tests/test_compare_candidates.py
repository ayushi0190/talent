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
from starlette.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_304_NOT_MODIFIED
from src.tests.test_helpers import TestHelpers
from src.utilities.custom_logging import CustomizeLogger

test_helper = TestHelpers()

logger = CustomizeLogger.make_logger()


class TestCompareCandidatesServices:
    """
    Test TestCompareCandidatesServices
    """

    def create_pass_payload(self, clt_id, test_app):
        """
        Test compare candidates success payload
        :param test_app:
        :param clt_id:
        :return:
        """
        success_payload = {}
        parse_job_response = test_helper.parse_fake_job(clt_id, test_app)
        parse_job_response = parse_job_response.json()
        if parse_job_response.get('code') == HTTP_200_OK or parse_job_response.get('code') == HTTP_304_NOT_MODIFIED:
            parse_resume_response = test_helper.parse_fake_resume(clt_id, test_app)
            parse_resume_response = parse_resume_response.json()
            if parse_resume_response.get('code') == HTTP_200_OK or parse_resume_response.get('code') == HTTP_304_NOT_MODIFIED:
                success_payload.update({
                    'JobId': test_helper.get_last_parsed_job_id(),
                    'resume_id': [test_helper.get_last_parsed_resume_id()]
                })
        return success_payload

    def create_payload(self, param=''):
        """
        Create Payload
        :param param: String
        :return:
        """
        fake = Faker()
        if param == 'job_id':
            job_id = ''
        else:
            job_id = fake.pystr(4).upper() + '-J-' + fake.pystr(4).upper() + '-' \
                     + fake.pystr(4, 11).upper() + '-' + str(fake.pyint(10)) + '-' \
                     + str(fake.pyint(3))
        if param == 'resume_id':
            resume_id = ''
        else:
            resume_id_one = fake.pystr(4).upper() + '-R-' + str(fake.pyint(10)) + '-' \
                            + fake.pystr(4).upper() + '-' + fake.pystr(4, 11).upper() + '-' \
                            + str(fake.pyint(3))
            resume_id_two = fake.pystr(4).upper() + '-R-' + str(fake.pyint(10)) + '-' \
                            + fake.pystr(4).upper() + '-' + fake.pystr(4, 11).upper() + '-' \
                            + str(fake.pyint(3))
            resume_id = [resume_id_one, resume_id_two]
        return {
            "JobId": job_id,
            "resume_id": resume_id
        }

    def test_compare_candidates_success(self, test_app):
        """
        Test success
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first
        # Matching Jobs
        logger.info("************************************* Start of Compare Candidates test case***************************************")
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        success_payload = self.create_pass_payload(authorization_response.get('client_id'), test_app)
        if success_payload:
            response_register = test_app.post('/compare/candidates', headers=headers,
                                              data=json.dumps(success_payload))
            if response_register.status_code == HTTP_200_OK:
                # Try to assert the token value received
                response_result = response_register.json()
                logger.info("***********************************Pass test case for Compare Candidates****************************")
                logger.info("Code we expect is 200, code we receive is:{}".format(response_register.status_code))
            else:
                assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
                logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))
            delete_resume = test_helper.delete_fake_resume(authorization_response.get('client_id'),
                                                           test_helper.get_last_parsed_resume_id(), test_app)
            assert delete_resume.status_code == HTTP_200_OK
            delete_job = test_helper.delete_fake_job(authorization_response.get('client_id'),
                                                     test_helper.get_last_parsed_job_id(), test_app)
            assert delete_resume.status_code == HTTP_200_OK

    def test_compare_candidates_fails_for_job_id(self, test_app):
        """
        Test failure for job id
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))

        response_register = test_app.post('/compare/candidates', headers=headers,
                                          data=self.create_payload('job_id'))

        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Compare Candidates Fails For Absent Of Job Id*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'JobId is not provided'
            logger.info("***************************************************************")

        else:
            logger.info("*******Compare Candidates Fails For Absent Of Job Id*******")
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_compare_candidates_fails_for_resume_id(self, test_app):
        """
        Test failure for resume ids
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/compare/candidates', headers=headers,
                                          data=self.create_payload('resume_id'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Compare Candidates Fails For Absent Of Resume Id's*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'resume_id is not provided'
            logger.info("***************************************************************")
        else:
            logger.info("*******Compare Candidates Fails For Absent Of Resume Id's*******")
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

        logger.info("************************************* End of Compare Candidates test case***************************************")