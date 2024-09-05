# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Test helpers
@author <rchakraborty@simplifyvms.com>
"""
from src.tests.base_case import test_app
from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from src.db.crud.sovren.prs_jobs_inf_schema import PrsJobInfSchema
from src.services.common.config.common_config import common_url_settings
import docx2txt
import requests
import base64
import json
import pdb
from faker import Faker


class TestHelpers:
    """
    Test helpers class
    """

    def get_last_parsed_resume_id(self):
        """
        Get the resume_id last parsed
        :return:
        """
        result = PrsResInfSchema.get_latest_inserted_record()
        return result.res_id

    def get_last_parsed_job_id(self):
        """
        Get the job_id last parsed
        :return:
        """
        result = PrsJobInfSchema().get_latest_inserted_record()
        return result.job_id

    def parse_fake_resume(self, clt_id, test_app):
        """
        Parse fake resume
        :param test_app:
        :param clt_id:
        :return:
        """
        text_resume = docx2txt.process('src/tests/fake_resume_and_job/test_resume.docx')
        base64_encoded_string = base64.b64encode(text_resume.encode())
        payload = {
            "index_id": "",
            "document_as_base_64_string": base64_encoded_string.decode('utf-8')
        }
        headers = {
            "Content-Type": "application/json",
            "client_id": clt_id
        }
        parse_response = test_app.post('/parse/resume', headers=headers,
                                       data=json.dumps(payload))
        return parse_response

    def delete_fake_resume(self, clt_id, resume_id, test_app):
        """
        Delete fake resume
        :param test_app:
        :param clt_id:
        :param resume_id:
        :return:
        """
        payload = {
            "resume_id": resume_id,
            "delete_index": True,
        }
        headers = {
            "Content-Type": "application/json",
            "client_id": clt_id
        }
        parse_response = test_app.post('/delete/resume', headers=headers,
                                       data=json.dumps(payload))
        return parse_response

    def parse_fake_job(self, clt_id, test_app):
        """
        Parse fake job
        :param test_app:
        :param clt_id:
        :return:
        """
        job_details = self.add_job_in_job_board()

        payload = {
            "job_id": job_details["result"]["job_reference_number"]
        }
        headers = {
            "Content-Type": "application/json",
            "client_id": clt_id
        }
        parse_response = test_app.post('/parse/job/by/id', headers=headers,
                                       data=json.dumps(payload))
        return parse_response

    def add_job_in_job_board(self):
        """
        Add Job in Job Board
        :return:
        """
        fake = Faker()
        text_job = docx2txt.process('src/tests/fake_resume_and_job/test_job.docx')
        base64_encoded_string = base64.b64encode(text_job.encode())

        headers = {"Authorization": common_url_settings.get("JOB_BOARD_AUTHORIZATION"),
                   "Content-Type": "application/json"}

        payload = {"source_job_id": 3333,
                   "source_id": "EX",
                   "job_title": "Test Data Scientist",
                   "job_type": "Temporary",
                   "job_category": "IT",
                   "hire_type": "Temp Hire",
                   "company_name": "Test",
                   "job_start_date": fake.date_between(start_date='+7d', end_date='+30d').strftime('%Y-%m-%d'),
                   "job_description": base64_encoded_string.decode('utf-8'),
                   "publish_status": "1",
                   "shift_start_time": "09:00",
                   "shift_end_time": "17:00",
                   "rate_type": "Weekly",
                   "job_publish_date": fake.date_between(start_date='-1m', end_date='today').strftime(
                       '%Y-%m-%d %H:%M:%S'),
                   "work_locations": "{\"work_location_name\":\"USA\"}"
                   }

        parse_job_response = requests.request("POST", url=common_url_settings.get("JOB_BOARD_JOB_PARSING_URL"),
                                              headers=headers,
                                              data=json.dumps(payload))
        return parse_job_response.json()

    def delete_fake_job(self, clt_id, job_id, test_app):
        """
        Delete fake job
        :param test_app:
        :param clt_id:
        :param job_id:
        :return:
        """
        payload = {
            "job_id": job_id,
            "delete_index": True,
        }
        headers = {
            "Content-Type": "application/json",
            "client_id": clt_id
        }

        parse_response = test_app.post('/delete/job', headers=headers,
                                       data=json.dumps(payload))
        return parse_response

    def parse_fake_job_by_description(self, clt_id, test_app):
        """
        Parse fake job
        :param test_app:
        :param clt_id:
        :return:
        """
        job_description = self.add_job_in_job_board()

        payload = {
            "job_title": "ML Engineer",
            "job_description": job_description["result"]["job_description"],
            "client_name": "TESTAI",
            "work_location": [
                {
                    "country": "USA",
                    "city": "Richardson",
                    "state": "Texas",
                    "zip": "TX 75082"
                }
            ]
        }
        headers = {
            "Content-Type": "application/json",
            "client_id": clt_id
        }
        parse_response = test_app.post('/parse/job/by/description', headers=headers,
                                       data=json.dumps(payload))
        return parse_response
