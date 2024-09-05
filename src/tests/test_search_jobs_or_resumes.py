# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Search jobs or resumes
@author <rchakraborty@simplifyvms.com>
"""
import json
import random

from universities import API

from faker import Faker
from src.tests.base_case import test_app
from src.tests.fake_client_registration import FakeClientRegistration
import logging
from src.utilities.custom_logging import CustomizeLogger
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_422_UNPROCESSABLE_ENTITY, \
    HTTP_304_NOT_MODIFIED
logger = CustomizeLogger.make_logger()


class TestSearchJobsResumesServices:
    """
    Test TestSearchJobsResumesServices
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

    def create_success_payload(self):
        """
        Create Payload
        :param param: String
        :return:
        """
        data = json.dumps({
            "Titles": ["Software Developer","Software Engineer"],
            "Skills": ["PHP","JAVA","C","Cpp","python"],
            "BucketType": "Job",
            "Location": "Newyork Us",
            "BucketId": ["SIMP-J-HIRE-THEROMOFISHER"]
        })
        return data

    def create_payload(self, param=''):
        """
        Create Payload
        :param param: String
        :return:
        """
        fake = Faker()
        if param == 'titles':
            titles = ''
        else:
            titles = str(fake.job())
        if param == 'skills':
            skills = ''
        else:
            skills = ["Python", "Java", "PHP"]
        if param == 'bucket_type_job':
            bucket_type = 'Resume'
        elif param == 'bucket_type_resume':
            bucket_type = 'Job'
        else:
            bucket_type = ''
        if param == 'location':
            location = ''
        else:
            location = fake.city() + ', ' + fake.country()
        if param == 'bucket_id':
            bucket_id = ''
        else:
            bucket_id = fake.pylist()
        if param == 'count':
            count = 0
        else:
            count = fake.pyint()
        if param == 'applied_jobs':
            applied_jobs = ''
        else:
            applied_jobs = fake.pylist()
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
        if param == 'max_date_range':
            max_date_range = ''
        else:
            max_date_range = fake.date()
        if param == 'min_date_range':
            min_date_range = ''
        else:
            min_date_range = fake.date()
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
            months_exp_min = fake.pyint()
        if param == 'months_exp_max':
            months_exp_max = ''
        else:
            months_exp_max = fake.pyint()
        if param == 'months_manage_exp_max':
            months_manage_exp_max = ''
        else:
            months_manage_exp_max = fake.pyint()
        if param == 'months_manage_exp_min':
            months_manage_exp_min = ''
        else:
            months_manage_exp_min = fake.pyint()
        if param == 'exec_type':
            exec_type = ''
        else:
            exec_type = fake.pylist(2, True, "str")
        if param == 'certifications':
            certifications = ''
        else:
            certifications = fake.pylist(2, True, "str")
        return {
            "Titles": [
                titles
            ],
            "Skills": skills,
            "BucketType": bucket_type,
            "Location": location,
            "BucketId": bucket_id,
            "Count": count,
            "AppliedJobs": applied_jobs,
            "SkillsMustAllExist": skills_must_all_exist,
            "Employers": [
                employers
            ],
            "EmployersMustAllBeCurrentEmployer": employers_must_all_be_current_employer,
            "DateRange": {
                "Minimum": min_date_range,
                "Maximum": max_date_range
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
            "DocumentLanguages": [
                document_languages
            ],
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
        }

    def test_successful_for_match_jobs_to_job(self, test_app):
        """
        Test successful Match Jobs To Job
        :param test_app:
        :return:
        """
        logger.info("************************************* Start of Search Jobs and Resumes test case***************************************")
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))

        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_success_payload())

        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("***********************************Pass Test Case for Search Jobs or Resumes****************************")
            logger.info("Code we expect is 200, code we receive is:{}".format(response_register.status_code))
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_titles(self, test_app):
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

        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('titles'))

        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Titles*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Titles****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_skills(self, test_app):
        """
        Test failure for skills
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('skills'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Skills*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Skills****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_bucket_type_job(self, test_app):
        """
        Test failure for bucket type job
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('bucket_type_job'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Bucket Type Job*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Bucket Type****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_bucket_type_resume(self, test_app):
        """
        Test failure for bucket type resume
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('bucket_type_resume'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Bucket Type Resume*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Bucket Type****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_location(self, test_app):
        """
        Test failure for location
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('location'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Location*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Location****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_bucket_id(self, test_app):
        """
        Test failure for bucket id
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('bucket_id'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Bucket Id*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Bucket Id****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_count(self, test_app):
        """
        Test failure for count
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('count'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Count*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Count****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_applied_jobs(self, test_app):
        """
        Test failure for applied jobs
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('applied_jobs'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Applied Jobs*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Applied Jobs****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_skills_must_all_exist(self, test_app):
        """
        Test failure for skills must all exist
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('skills_must_all_exist'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Skills Must All Exist*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Skills Must All Exist****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_employers(self, test_app):
        """
        Test failure for absence of employers
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('employers'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Employers*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Employers****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_employers_must_all_be_current_employer(self, test_app):
        """
        Test failure for employers must all be current employer
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('employers_must_all_be_current_employer'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Employers Must All Be Current Employer*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            logger.info("**************************************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Employers Must All Be Current Employer****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_date_range_max(self, test_app):
        """
        Test failure for date range max
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('date_range_max'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Date Range Max*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Date Range Max****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_date_range_min(self, test_app):
        """
        Test failure for date range min
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('date_range_min'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Date Range Min*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Date Range Min****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_school_name(self, test_app):
        """
        Test failure for school name
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('school_name'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of School Name*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of School Name****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_degree_major(self, test_app):
        """
        Test failure for degree major
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('degree_major'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Degree Major*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Degree Major****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_degree_type(self, test_app):
        """
        Test failure for degree type
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('degree_type'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Degree Type*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Degree Type****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_degree_name(self, test_app):
        """
        Test failure for degree name
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('degree_name'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Degree Name*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Degree Name****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_minimum_gpa(self, test_app):
        """
        Test failure for minimum GPA
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('minimum_GPA'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Minimum GPA*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Minimum GPA****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_country_code(self, test_app):
        """
        Test failure for country code
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('country_code'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Country Code*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Country Code****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_region(self, test_app):
        """
        Test failure for region
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('region'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Region*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Region****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_municipality(self, test_app):
        """
        Test failure for municipality
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('municipality'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Municipality*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Municipality****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_postal_code(self, test_app):
        """
        Test failure for postal code
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('postal_code'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Postal Code*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Postal Code****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_latitude(self, test_app):
        """
        Test failure for latitude
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('latitude'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Latitude*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Latitude****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_longitude(self, test_app):
        """
        Test failure for longitude
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('longitude'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Longitude*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Longitude****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_distance(self, test_app):
        """
        Test failure for distance
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('distance'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Distance*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Distance****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_distance_unit(self, test_app):
        """
        Test failure for distance
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('distance_unit'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Distance Unit*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Distance Unit****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_geocode_provider(self, test_app):
        """
        Test failure for geocode provider
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('geocode_provider'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Geocode Provider*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Geocode Provider****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_geocode_provider_key(self, test_app):
        """
        Test failure for geocode provider key
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('geocode_provider_key'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Geocode Provider Key*******")
            assert response_result['code'] == 400
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Geocode Provider Key****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_search_expression(self, test_app):
        """
        Test failure for search expression
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('search_expression'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Search Expression*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of  Search Expression****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_languages_known(self, test_app):
        """
        Test failure for languages known
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('languages_known'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Languages Known*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Languages Known****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_languages_known_must_all_exist(self, test_app):
        """
        Test failure for languages known must all exist
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('languages_known_must_all_exist'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Languages Known Must All Exist*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Languages Known Must All Exist****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_current_management_level(self, test_app):
        """
        Test failure for current management level
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('current_management_level'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Current Management Level*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Current Management Level****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_document_languages(self, test_app):
        """
        Test failure for document languages
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('document_languages'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Document Languages*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Document Languages****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_months_exp_min(self, test_app):
        """
        Test failure for months of minimum experience
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('months_exp_min'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Months Of Minimum Experience*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            logger.info("****************************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Months Of Minimum Experience****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_months_exp_max(self, test_app):
        """
        Test failure for months of maximum experience
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('months_exp_max'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Months Of Maximum Experience*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            logger.info("****************************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Months Of Maximum Experience****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_months_manage_exp_min(self, test_app):
        """
        Test failure for months of minimum management experience
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('months_manage_exp_min'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Months Of Minimum Management Experience*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            logger.info("***************************************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Months Of Minimum Management Experience****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_months_manage_exp_max(self, test_app):
        """
        Test failure for months of maximum management experience
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('months_manage_exp_max'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Months Of Maximum Management Experience*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            logger.info("***************************************************************************************")
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Months Of Maximum Management Experience****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_exec_type(self, test_app):
        """
        Test failure for exec type
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('exec_type'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Exec Type*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'
            
        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Exec Type****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

    def test_match_jobs_fails_for_certifications(self, test_app):
        """
        Test failure for certifications
        :param test_app:
        :return:
        """
        # Sample payload needs to be created first

        # Matching Jobs
        fake_registration = FakeClientRegistration()
        authorization_response = fake_registration.register_client(test_app)
        headers = fake_registration.request_headers(authorization_response.get('client_id'))
        response_register = test_app.post('/search/jobs/resumes', headers=headers,
                                          data=self.create_payload('certifications'))
        if response_register.status_code == 200:
            # Try to assert the token value received
            response_result = response_register.json()
            logger.info("*******Searching Jobs or Resume Fails For Absent Of Certifications*******")
            if not response_result.get('detail').get('data'):
                assert response_result.get('detail').get('error') == 'you have not permission to access this service'

        else:
            assert response_register.status_code == HTTP_422_UNPROCESSABLE_ENTITY
            logger.info("***********************************Searching Jobs or Resume Fails For Absent Of Certifications****************************")
            logger.info("Code we expect is 422, code we receive is:{}".format(response_register.status_code))

        logger.info("************************************* End of Search Jobs and Resumes test case***************************************")