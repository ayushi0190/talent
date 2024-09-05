# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Matching jobs test
@author <rchakraborty@simplifyvms.com>
@author <sreddy@simplifyvms.com>
"""
import json
import random
import logging
from universities import API
from faker import Faker
from src.tests.base_case import test_app
from src.tests.fake_client_registration import FakeClientRegistration
from src.db.models.sovren.prs_res_inf import PrsResInfModel
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_304_NOT_MODIFIED, HTTP_400_BAD_REQUEST
from src.tests.test_helpers import TestHelpers
from src.utilities.custom_logging import CustomizeLogger

test_helper = TestHelpers()

logger = CustomizeLogger.make_logger()


class TestMatchJobsToResumeMatcherServices:
    """
    Test TestMatchJobsToResumeMatcherServices
    """

    def get_univesities_name(self, country):
        """
        Get the Universities name of a country
        :param country:
        :return:
        """
        univs = []
        uni = API()
        univ_search = uni.search(name=country)
        for data in univ_search:
            univs.append(data.name)
        return univs

    def create_payload(self, param=''):
        """
        Create Payload
        :param param: String
        :return:
        """
        fake = Faker()
        if param == 'job_id':
            job_id = 'SIMP-J-HIRE-SIMPLIFYVMS-' + str(fake.pyint()) + '-' + str(fake.pyint())
        else:
            job_id = 'SIMP-J-HIRE-SIMPLIFYVMS-1592581078-162'
        if param == 'no_of_matches':
            no_of_matches = ''
        else:
            no_of_matches = fake.pyint()
        if param == 'refresh_rate':
            refresh_rate = ''
        else:
            refresh_rate = fake.pyint()
        if param == 'titles':
            titles = ''
        else:
            titles = fake.job()
        if param == 'skills':
            skills = ''
        else:
            skills = ["Python", "PHP", "Java"]
        if param == 'skills_must_all_exist':
            skills_must_all_exist = ''
        else:
            skills_must_all_exist = fake.pybool()
        if param == 'employers':
            employers = ''
        else:
            employers = fake.company()
        if param == 'employers_must_all_be_current_employer':
            employers_must_all_be_current_employer = ''
        else:
            employers_must_all_be_current_employer = fake.pybool()
        if param == 'date_range_max':
            date_range_max = ''
        else:
            date_range_max = fake.date()
        if param == 'date_range_min':
            date_range_min = ''
        else:
            date_range_min = fake.date()
        if param == 'school_name':
            school_name = ''
        else:
            univs = self.get_univesities_name("India")
            school_name = random.choice(univs[0])
        if param == 'degree_major':
            degree_major = ''
        else:
            degree_major = "Computers"
        if param == 'degree_name':
            degree_name = ''
        else:
            degree_name = "B.Tech"
        if param == 'degree_type':
            degree_type = ''
        else:
            degree_type = "Regular"
        if param == 'minimum_GPA':
            minimum_GPA = ''
        else:
            minimum_GPA = fake.pyint()
        if param == 'country_code':
            country_code = ''
        else:
            country_code = fake.country_code()
        if param == 'region':
            region = ''
        else:
            region = fake.street_address()
        if param == 'municipality':
            municipality = ''
        else:
            municipality = fake.city()
        if param == 'postal_code':
            postal_code = ''
        else:
            postal_code = fake.postcode()
        if param == 'latitude':
            latitude = ''
        else:
            latitude = float(fake.latitude())
        if param == 'longitude':
            longitude = ''
        else:
            longitude = float(fake.longitude())
        if param == 'distance':
            distance = ''
        else:
            distance = fake.pyint()
        if param == 'distance_unit':
            distance_unit = ''
        else:
            distance_unit = "Mile"
        if param == 'geocode_provider':
            geocode_provider = ''
        else:
            geocode_provider = fake.pystr()
        if param == 'geocode_provider_key':
            geocode_provider_key = ''
        else:
            geocode_provider_key = fake.pystr_format()
        if param == 'search_expression':
            search_expression = ''
        else:
            search_expression = 'skill:' + fake.pystr() + ' AND \"' + fake.pystr() + '\"'
        if param == 'languages_known':
            languages_known = ''
        else:
            languages_known = fake.language_name()
        if param == 'languages_known_must_all_exist':
            languages_known_must_all_exist = ''
        else:
            languages_known_must_all_exist = fake.pybool()
        if param == 'current_management_level':
            current_management_level = ''
        else:
            current_management_level = fake.pystr()
        if param == 'document_languages':
            document_languages = ''
        else:
            document_languages = fake.pylist(2, True, "str")
        if param == 'months_exp_min':
            months_exp_min = ''
        else:
            months_exp_min = fake.date()
        if param == 'months_exp_max':
            months_exp_max = ''
        else:
            months_exp_max = fake.date()
        if param == 'months_manage_exp_max':
            months_manage_exp_max = ''
        else:
            months_manage_exp_max = fake.date()
        if param == 'months_manage_exp_min':
            months_manage_exp_min = ''
        else:
            months_manage_exp_min = fake.date()
        if param == 'exec_type':
            exec_type = ''
        else:
            exec_type = fake.pylist(2, True, "str")
        if param == 'certifications':
            certifications = ''
        else:
            certifications = fake.pylist(2, True, "str")
        return json.dumps({
            "job_id": job_id,
            "no_of_matches": no_of_matches,
            "refresh_rate": refresh_rate,
            "Titles": [
                titles
            ],
            "Skills": skills,
            "SkillsMustAllExist": skills_must_all_exist,
            "Employers": [
                employers
            ],
            "EmployersMustAllBeCurrentEmployer": employers_must_all_be_current_employer,
            "DateRange": {
                "Minimum": date_range_max,
                "Maximum": date_range_min
            },
            "Educations": [
                {
                    "SchoolName": school_name,
                    "DegreeMajor": degree_major,
                    "DegreeName": degree_name,
                    "DegreeType": degree_type,
                    "MinimumGPA": minimum_GPA
                }
            ],
            "LocationCriteria": {
                "Locations": [
                    {
                        "CountryCode": country_code,
                        "Region": region,
                        "Municipality": municipality,
                        "PostalCode": postal_code,
                        "Geopoint": {
                            "Latitude": latitude,
                            "Longitude": longitude
                        }
                    }
                ],
                "Distance": distance,
                "DistanceUnit": distance_unit,
                "GeocodeProvider": geocode_provider,
                "GeocodeProviderKey": geocode_provider_key
            },
            "SearchExpression": search_expression,
            "SchoolNames": [
                school_name
            ],
            "DegreeNames": [
                degree_name
            ],
            "DegreeTypes": [
                degree_type
            ],
            "LanguagesKnown": [
                languages_known
            ],
            "LanguagesKnownMustAllExist": languages_known_must_all_exist,
            "CurrentManagementLevel": current_management_level,
            "DocumentLanguages": document_languages,
            "MonthsExperience": {
                "Minimum": months_exp_min,
                "Maximum": months_exp_max
            },
            "MonthsManagementExperience": {
                "Minimum": months_manage_exp_min,
                "Maximum": months_manage_exp_max
            },
            "ExecutiveType": exec_type,
            "Certifications": certifications
        })

    def create_success_payload(self, resume_id):
        """
        Create Payload
        :param param: String
        :return:
        """

        data = json.dumps({
            "resume_id": resume_id,
            "no_of_matches": 10,
            "refresh_rate": 50
        })
        return data

    def test_successful_for_match_jobs_to_resume(self, test_app):
        """
        Test successful Match Jobs To Resume
        :param test_app:
        :return:
        """
        logger.info("************************************* Start of Match Jobs to Resume test case***************************************")
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = {
            "Content-Type": "application/json",
            "client_id": authorization_response.get('client_id')
        }
        resume_response = test_helper.parse_fake_resume(authorization_response.get('client_id'), test_app)
        response_result = resume_response.json()
        if response_result.get("code") == HTTP_200_OK or \
            response_result.get("code") == HTTP_304_NOT_MODIFIED:
            latest_test_resume = test_helper.get_last_parsed_resume_id()

            candidate_resume = test_app.post('/match/jobs/resume',
                                             headers=headers,
                                             data=self.create_success_payload(latest_test_resume))
            if candidate_resume.status_code == HTTP_200_OK:
                # Try to assert the token value received
                response_result = candidate_resume.json()
                response_result = response_result[0]
                assert response_result.get("code") == HTTP_200_OK or \
                       response_result.get("code") == HTTP_204_NO_CONTENT

                logger.info("***********************************Pass Test Case for Matching Jobs To Resume****************************")
                logger.info("Code we expect is 200 or 204, code we receive is:{}".format(response_result.get('code')))

                delete_resume = test_helper.delete_fake_resume(authorization_response.get('client_id'),
                                                               latest_test_resume, test_app)

                assert delete_resume.status_code == HTTP_200_OK
        else:
            assert response_result.get("code") == HTTP_404_NOT_FOUND
            logger.info("***********************************Failed Test Case for Matching Jobs To Resume****************************")
            logger.info("Code we expect is 404, code we receive is:{}".format(response_result.get('code')))

    def test_match_jobs_fails_for_false_resume_id(self, test_app):
        """
        Test Fail Match Jobs To Resume
        :param test_app:
        :return:
        """
        fake = Faker()
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        false_id = "SIMP-R-{}-HIRE-THERMOFISHER-{}".format(fake.random_int(1500000000, 1583916379),
                                                           fake.random_int())
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_success_payload(false_id))

        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            response_result = response_result[0]
            if int(response_result.get('code')) == HTTP_404_NOT_FOUND:
                assert response_result.get("code") == HTTP_404_NOT_FOUND
                logger.info("***********************************Matching Jobs To Resume Fails For Wrong Resume Id****************************")
                logger.info("Code we expect is 404, code we receive is:{}".format(response_result.get('code')))
            else:
                assert response_result.get("code") == HTTP_204_NO_CONTENT
                logger.info("***********************************Matching Jobs To Resume Fails For Wrong Resume Id****************************")
                logger.info("Code we expect is 204, code we receive is:{}".format(response_result.get('code')))
    def test_match_jobs_fails_for_resume_id(self, test_app):
        """
        Test failure for missing of resume_id
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('resume_id'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching jobs Fails For Absent Of Resume Id*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'resume_id is not provided'
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Resume Id****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_no_of_matches(self, test_app):
        """
        Test failure for absence of number of matches
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('no_of_matches'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs Fails For Absent Of Number Of Matches*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'no_of_matches is not provided'
            logger.info("***************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Number Of Matches****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_refresh_rate(self, test_app):
        """
        Test failure for refresh rate
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('refresh_rate'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs Fails For Absent Of Refresh Rate*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'refresh_rate is not provided'
            logger.info("***************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Refresh Rate****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_titles(self, test_app):
        """
        Test failure for titles
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('titles'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs Fails For Absent Of Titles*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'titles is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Titles****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_skills(self, test_app):
        """
        Test failure for skills
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('skills'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Skills*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'skills is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Skills****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_skills_must_all_exist(self, test_app):
        """
        Test failure for skills must all exist
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('skills_must_all_exist'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Skills Must All Exist*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'skills_must_all_exist is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Skilla Must All Exist****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_employers(self, test_app):
        """
        Test failure for absence of employers
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('employers'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Employers*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'employers is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Employers****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_employers_must_all_be_current_employer(self, test_app):
        """
        Test failure for employers must all be current employer
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('employers_must_all_be_current_employer'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info(
                "*******Matching Jobs To Resume Fails For Absent Of Employers Must All Be Current Employer*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get(
                    'error') == 'employers_must_all_be_current_employer is not provided'
            logger.info("**************************************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Employers Must All Be Current Employer****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_date_range_max(self, test_app):
        """
        Test failure for date range max
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('date_range_max'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Date Range Max*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'date_range_max is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of For Absent Of Date Range Max****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_date_range_min(self, test_app):
        """
        Test failure for date range min
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('date_range_min'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Date Range Min*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'date_range_min is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Date Range Min****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_school_name(self, test_app):
        """
        Test failure for school name
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('school_name'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of School Name*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'school_name is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of School Name****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_degree_major(self, test_app):
        """
        Test failure for degree major
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('degree_major'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Degree Major*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'degree_major is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Degree Major****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_degree_type(self, test_app):
        """
        Test failure for degree type
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('degree_type'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Degree Type*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'degree_type is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Degree Type****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_degree_name(self, test_app):
        """
        Test failure for degree name
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('degree_name'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs Fails For Absent Of Degree Name*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'degree_name is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Degree Name****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_minimum_gpa(self, test_app):
        """
        Test failure for minimum GPA
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('minimum_GPA'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Minimum GPA*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'minimum_GPA is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Minimum GPA****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_country_code(self, test_app):
        """
        Test failure for country code
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('country_code'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Country Code*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'country_code is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Country Code****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_region(self, test_app):
        """
        Test failure for region
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('region'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Region*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'region is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Region****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_municipality(self, test_app):
        """
        Test failure for municipality
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('municipality'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Municipality*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'municipality is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Municipality****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_postal_code(self, test_app):
        """
        Test failure for postal code
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('postal_code'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Postal Code*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'postal_code is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Postal Code****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_latitude(self, test_app):
        """
        Test failure for latitude
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('latitude'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Latitude*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'latitude is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Latitude****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_longitude(self, test_app):
        """
        Test failure for longitude
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('longitude'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Longitude*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'longitude is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Longitude****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_distance(self, test_app):
        """
        Test failure for distance
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('distance'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Distance*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'distance is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Distance****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_distance_unit(self, test_app):
        """
        Test failure for distance
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('distance_unit'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Distance Unit*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'distance_unit is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Distance Unit****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_geocode_provider(self, test_app):
        """
        Test failure for geocode provider
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('geocode_provider'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Geocode Provider*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'geocode_provider is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Geocode Provider****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_geocode_provider_key(self, test_app):
        """
        Test failure for geocode provider key
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('geocode_provider_key'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Geocode Provider Key*******")
            assert response_result['code'] == HTTP_400_BAD_REQUEST
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'geocode_provider_key is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Geocode Provider Key****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_search_expression(self, test_app):
        """
        Test failure for search expression
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('search_expression'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Search Expression*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'search_expression is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Search Expression****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_languages_known(self, test_app):
        """
        Test failure for languages known
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('languages_known'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Languages Known*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'languages_known is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Languages Known****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_languages_known_must_all_exist(self, test_app):
        """
        Test failure for languages known must all exist
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('languages_known_must_all_exist'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Languages Known Must All Exist*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'languages_known_must_all_exist is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Languages Known Must All Exist****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_current_management_level(self, test_app):
        """
        Test failure for current management level
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('current_management_level'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Current Management Level*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'current_management_level is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Current Management Level****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_document_languages(self, test_app):
        """
        Test failure for document languages
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('document_languages'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Document Languages*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'document_languages is nor provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Document Languages****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_months_exp_min(self, test_app):
        """
        Test failure for months of minimum experience
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('months_exp_min'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Months Of Minimum Experience*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'months_exp_min is not provided'
            logger.info("****************************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Months Of Minimum Experience****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_months_exp_max(self, test_app):
        """
        Test failure for months of maximum experience
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('months_exp_max'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Months Of Maximum Experience*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'months_exp_max is not provided'
            logger.info("****************************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Months Of Maximum Experience****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_months_manage_exp_min(self, test_app):
        """
        Test failure for months of minimum management experience
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('months_manage_exp_min'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info(
                "*******Matching Jobs To Resume Fails For Absent Of Months Of Minimum Management Experience*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'months_manage_exp_min is not provided'
            logger.info("***************************************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Months Of Minimum Management Experience****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_months_manage_exp_max(self, test_app):
        """
        Test failure for months of maximum management experience
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('months_manage_exp_max'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info(
                "*******Matching Jobs To Resume Fails For Absent Of Months Of Maximum Management Experience*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'months_manage_exp_max is not provided'
            logger.info("***************************************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Months Of Maximum Management Experience****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_exec_type(self, test_app):
        """
        Test failure for exec type
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('exec_type'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Exec Type*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'exec_type is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Exec Type****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_to_resume_fails_for_certifications(self, test_app):
        """
        Test failure for certifications
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs To Resume
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/match/jobs/resume', headers=headers,
                                          data=self.create_payload('certifications'))
        if response_register.status_code == HTTP_200_OK:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Matching Jobs To Resume Fails For Absent Of Certifications*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'certifications is not provided'
            logger.info("***************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Matching Jobs To Resume Fails For Absent Of Certifications****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

        logger.info("************************************* End of Match Jobs to Resume test case***************************************")