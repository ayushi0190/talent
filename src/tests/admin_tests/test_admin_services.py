# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Register client test
@author <rchakraborty@simplifyvms.com>
"""
import json
from faker import Faker
from src.tests.base_case import test_app
import logging
from starlette.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY

logger = logging.getLogger('faker')
logger.setLevel(logging.INFO)

class TestAdminServices:
    """
    Test AdminServices
    """
    logger.info("************************************* Start of Admin Services test case***************************************")
    def create_payload(self, param=''):
        """
        Create Payload
        :param param: String
        :return:
        """
        fake = Faker()
        if param == 'company_name':
            company_name = ''
        else:
            company_name = fake.company()
        if param == 'registration_date':
            registration_date = ''
        else:
            registration_date = fake.date_between(start_date='-2m', end_date='today').strftime('%Y-%m-%d')
        if param == 'contract_period':
            contract_period = ''
        else:
            contract_period = fake.pyint()
        if param == 'parsing':
            parsing = ''
        else:
            parsing = fake.pybool()
        if param == 'matching':
            matching = ''
        else:
            matching = fake.pybool()
        if param == 'searching':
            searching = ''
        else:
            searching = fake.pybool()
        if param == 'scoring':
            scoring = ''
        else:
            scoring = fake.pybool()
        if param == 'parse_job':
            parse_job = ''
        else:
            parse_job = fake.pybool()
        if param == 'parse_resume':
            parse_resume = ''
        else:
            parse_resume = fake.pybool()
        if param == 'similar_jobs':
            similar_jobs = ''
        else:
            similar_jobs = fake.pybool()
        if param == 'discover_candidates':
            discover_candidates = ''
        else:
            discover_candidates = fake.pybool()
        if param == 'suggested_candidates':
            suggested_candidates = ''
        else:
            suggested_candidates = fake.pybool()
        if param == 'suggested_jobs':
            suggested_jobs = ''
        else:
            suggested_jobs = fake.pybool()
        if param == 'compare_candidates':
            compare_candidates = ''
        else:
            compare_candidates = fake.pybool()
        if param == 'get_parsed_resume':
            get_parsed_resume = ''
        else:
            get_parsed_resume = fake.pybool()
        if param == 'get_parsed_job':
            get_parsed_job = ''
        else:
            get_parsed_job = fake.pybool()
        if param == 'search_jobs':
            search_jobs = ''
        else:
            search_jobs = fake.pybool()
        if param == 'score_resume_job':
            score_resume_job = ''
        else:
            score_resume_job = fake.pybool()
        if param == 'sovren':
            sovren = ''
        else:
            sovren = fake.pybool()
        if param == 'opening':
            opening = ''
        else:
            opening = fake.pybool()
        if param == 'simpai':
            simpai = ''
        else:
            simpai = fake.pybool()
        if param == 'pol_shr':
            pol_shr = ''
        else:
            pol_shr = fake.pybool()
        if param == 'pol_prv':
            pol_prv = ''
        else:
            pol_prv = fake.pybool()

        return json.dumps({
            "company_name": company_name,
            "registration_date": registration_date,
            "contract_period": contract_period,
            "pol_shr": pol_shr,
            "pol_prv": pol_prv,
            "services_to_use": {
                "parsing": parsing,
                "matching": matching,
                "searching": searching,
                "scoring": scoring,
                "parser_service_to_use": {
                    "parse_job": parse_job,
                    "parse_resume": parse_resume
                },
                "matcher_service_to_use": {
                    "similar_jobs": similar_jobs,
                    "discover_candidates": discover_candidates,
                    "suggested_candidates": suggested_candidates,
                    "suggested_jobs": suggested_jobs,
                    "compare_candidates": compare_candidates
                },
                "searcher_services_to_use": {
                    "get_parsed_resume": get_parsed_resume,
                    "get_parsed_job": get_parsed_job,
                    "search_jobs": search_jobs
                },
                "scorer_services_to_use": {
                    "score_resume_job": score_resume_job
                }
            },
            "tool_to_use": {
                "sovren": sovren,
                "opening": opening,
                "simpai": simpai
            }
        })

    def test_successful_register_client(self, test_app):
        """
        Test successful client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload())
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Register Client Successful Test Case*******")
            assert response_register.status_code == HTTP_200_OK
            if response_result['client_id'] is not None:
                assert type(response_result['client_id']) == str
            logger.info("***************************************************")

    def test_register_client_fails_for_company_name(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('company_name'))

        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Company Name*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'Must be of string type'
        logger.info("***************************************************")

    def test_register_client_fails_for_registration_date(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('registration_date'))

        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Registration Date*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'invalid date format'
        logger.info("***************************************************")

    def test_register_client_fails_for_contract_period(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('contract_period'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Contract Period*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value is not a valid integer'
        logger.info("***************************************************")

    def test_register_client_fails_for_pol_shr(self, test_app):
        """
        Test failure for shared pool
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('pol_shr'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Shared Pool*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************")

    def test_register_client_fails_for_pol_prv(self, test_app):
        """
        Test failure for private pool
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('pol_prv'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Private Pool*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************")

    def test_register_client_fails_for_parsing(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('parsing'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Parsing Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_matching(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('matching'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Matching Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_searching(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('searching'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Searching Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_scoring(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('scoring'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Scoring Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_parse_job(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('parse_job'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Parse Job Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_parse_resume(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('parse_resume'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Parse Resume Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_similar_jobs(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('similar_jobs'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Similar Jobs Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_discover_candidates(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('discover_candidates'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Discover Candidates Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_suggested_candidates(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('suggested_candidates'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Suggested Candidates Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_suggested_jobs(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('suggested_jobs'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Suggested Jobs Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_compare_candidates(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('compare_candidates'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Compare Candidates Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_get_parsed_resume(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('get_parsed_resume'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Get Parsed Resume Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_get_parsed_job(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('get_parsed_job'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Get Parsed Job Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_search_jobs(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('search_jobs'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Search Job Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_score_resume_job(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('score_resume_job'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Score Resume Job Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_sovren(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('sovren'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Sovren Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_opening(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('opening'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Opening Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    def test_register_client_fails_for_simpai(self, test_app):
        """
        Test failure client registration
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Register client
        response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                          data=self.create_payload('simpai'))
        # Try to assert the token value received
        response_result = response_register.json()
        logger.info("*******Register Client Fails For Absent Of Simpai Value*******")
        assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
        assert response_result['detail'][0]['msg'] == 'value could not be parsed to a boolean'
        logger.info("***************************************************************")

    logger.info("************************************* End of Admin Services test case***************************************")