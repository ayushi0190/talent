import base64
import json
import requests
from datetime import datetime
import arrow
from requests.exceptions import RequestException
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_409_CONFLICT, HTTP_304_NOT_MODIFIED
# from src.db.crud.sovren.job_parser_schema import JobsToJobSchema
from src.services.common.apis.job_board_services import JobBoardServices
from src.db.crud.sovren.prs_jobs_inf_schema import PrsJobInfSchema
from src.db.crud.common.matching_index_schema import MatchingIndexSchema
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.config.common_config import common_url_settings
from src.services.common.helpers.misc_helpers import get_job_board_headers
from src.services.sovren.interfaces.parsers.job_parser_interface import \
    JobParserInterface
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema
from src.services.sovren.helpers.indexing_helper import job_indexer
from src.services.simpai.config.simpai_config import simpai_url_settings
from src.services.sovren.helpers.misc_helpers import (get_job_index)
import time
# from fastapi.logger import logger
# import logging
# logger = logging.getLogger(__name__)
from src.utilities.custom_logging import cust_logger as logger


class SimpJobParserServices(JobParserInterface):
    """
    Job Parser services
    """

    def __init__(self):
        self.job_parsed_resp = None
        self.parser = common_url_settings.get("SIMPAI_SERVICE")  # 'simplifyai'
        self.job_title = ''
        self.job_loc = ''
        self.job_type = ''
        self.job_cat = ''
        self.job_exp = ''

    def start_parse_job(self, client_id, job_details, job_id: str) -> dict:
        # client_id = request.headers["client_id"]
        return self.parse_job(client_id, job_details, job_id)
        pass

    def parse_job(self, client_id, job_details, job_id: str, parse_by_id=False) -> dict:
        """
        It checks whether JOB parsed or not
        param : request
        param : job_details
        param data: job_id
        :return: JSON output
        """
        request = None
        job_schema = PrsJobInfSchema()
        result = {}
        # Get Client ID from HEADERS
        # client_id = request.headers["client_id"]

        parsed_job_info = job_schema.get_by_parser(job_id, client_id,
                                                   self.parser)
        # Check if JOB_ID already exist in DB or not
        # If Job_id EXISTS in DB return response from DB
        if parse_by_id:
            display_data = json.loads(parsed_job_info.job_res)

            result.update({
                'data': display_data,
                'code': HTTP_200_OK
            })
            return result

        else:
            if parsed_job_info is not None:
                logger.info("JOB already exist in DB")

                # display_data = json.loads(parsed_job_info.job_res)
                # display_data = display_data.get('Value', {}).get('ParsedDocument', '')
                display_data = json.loads(parsed_job_info.job_res)

                result.update({
                    'code': HTTP_304_NOT_MODIFIED,
                    'message': "Duplicate JOB",
                    'data': display_data
                })
            else:
                # If Job_id does not Exists in DB
                logger.info("JOB does not exist in DB and need to Parse")  # + str(job_details))
                job_description_base64 = job_details.get("data").get("result")[0]. \
                    get("job").get("job_description_base64")
                job_info = job_details.get("data").get("result")[0].get("job", {})
                self.job_title = job_info.get("job_title", "")
                self.job_loc = job_info.get("job_location", "")
                self.job_type = job_info.get("job_type", "")
                self.job_cat = job_info.get("job_category", "")
                self.job_exp = job_info.get("job_experience", "")

                # Get the Job Index_id based on job_id
                job_index_id = get_job_index(job_id)
                logger.info("JOB index ID from get_job_index %s " % job_index_id)

                # No need to create index in Sovren for Simpai request
                # Check Job Index ID exist or not
                # job_index = job_indexer(request,job_index_id)
                job_index = {"code": HTTP_200_OK}

                # If Index returns success or it is already created
                # Call Parse Job
                if job_index.get("code") in [HTTP_200_OK, HTTP_409_CONFLICT]:
                    result = self.simpai_parse_job(request, job_description_base64,
                                                   job_index_id, job_id, client_id)
                    return result
                else:
                    # If job_index returns some error while creating an index
                    return job_index

        return result

    def convert_base64_to_string(self, base64str):
        """
        Convert base64 to text
        :param base64str: String
        :return: String
        """
        decoded_str = base64.b64decode(base64str).decode()
        return decoded_str

    def simpai_parse_job(self, request, job_document: str, job_index_id: str,
                         job_document_id: str, clt_id: str) -> dict:
        """
        Parse job with Simpai
        :param job_document_id: String
        :param job_index_id: String
        :param job_document: String
        :return:
        """
        # clt_id = request.headers['client_id']

        job_parser = PrsJobInfSchema()
        base_64_encoded_string = job_document
        job_desc = self.convert_base64_to_string(base_64_encoded_string)
        # revision_date = arrow.now().format("YYYY-MM-DD")
        index_id = job_index_id
        # document_id = job_document_id
        # with endpoint /v1/parse_job

        # with endpoint /v1/parse_jd
        payload = {
            "description": job_desc,
            "title": self.job_title,
            "location": self.job_loc,
            "jobType": self.job_type,
            "experience": self.job_exp,
            "category": self.job_cat,
            "skills": [],
            "config_flag": {
                "ALL_NORMALIZATION_FLAG": 'true',
                "NORMALIZE_SKILL_FLAG": 'true',
                "NORMALIZE_TITLES_FLAG": 'true',
                "NORMALIZE_EDUCATION_FLAG": 'true',
                "NORMALIZE_EXPERIENCE_FLAG": 'true',
                "NORMALIZE_LOCATION_FLAG": 'true',
                "CLASSIFY_INDUSTRY_FLAG": 'true',
                "SIMILAR_TITLES_FLAG": 'true',
                "SIMILAR_TITLES_ON_SKILLS_FLAG": 'true',
                "OLD_JSON": 'false',
                "TIME_LOG_FLAG": 'true'
            }
        }
        # logger.info("JD: {}".format(json.dumps(payload)))
        simpai_headers = {"accept": "application/json",
                          "content-type": "application/json",
                          "Authorization": "Bearer " + simpai_url_settings.get("SIMPAI_JOB_PARSER_AUTH_TOKEN", ''),
                          }  
        simpai_job_parser_url = simpai_url_settings.get("SIMPAI_JOB_PARSER_URL")
        logger.info("Job Parser URL: {}".format(simpai_job_parser_url))
        prs_start_time = datetime.now()
        # logger.info("Job Parser Payload : %s " % json.dumps(payload))
        start = time.time()
        result = self.connect_to_api(simpai_headers, payload,
                                     simpai_job_parser_url)
        prs_time_taken = (datetime.now() - prs_start_time).seconds
        if result.get("code") != HTTP_200_OK:
            return result

        # If a response from Sovren is 200
        if result.get("code") == HTTP_200_OK:
            formatted_result = {}
            data_to_save = job_parser.save_job(request, index_id, job_document_id,
                                               result.get('data'), clt_id, prs_time_taken, self.parser)

            if data_to_save:
                logger.info("Parsed JOB Saved in DB ")
                result.update({
                    "saved_in_DB": True
                })
            else:
                logger.info("Parsed JOB NOT Saved in DB ")
                result.update({
                    "saved_in_DB": False
                })
            display_data = json.loads(result.get('data'))
            # display_data = display_data.get('Value', {}).get('ParsedDocument', '')
            # display_data = json.loads(display_data)

            formatted_result.update({
                "code": result.get('code'),
                "message": result.get('message'),
                "data": display_data
            })
            result = formatted_result
            end = time.time()
            logger.info("Job Parser time taken for Simplifyai: %s " % (end - start))
            return result
        pass

    def connect_to_api(self, header: dict, payload: dict,
                       calling_api: str) -> dict:
        """
        Connect to Simpai API to parse job
        :param header: Dictionary
        :param payload: Dictionary
        :param calling_api: String
        :return:
        """
        result = {}
        try:
            response = requests.request(
                "POST", headers=header, data=json.dumps(payload), url=calling_api
            )
            if response.status_code == 200:
                response_info = response.json()

                result = {"code": HTTP_200_OK,
                          "message": "Successfully parsed the JOB",
                          "data": json.dumps(response_info)}
                logger.info("Successfully parsed the JOB ")
            else:
                result = {"code": response.status_code, \
                          "message": response.reason, \
                          "detail": response.text,
                          "error": "Simpai unable to process the Parse Job request"}
                logger.info("Simpai unable to process the Parse JOB request ")
            return result
        except Exception as ex:
            logger.info("Error while parsing JOB from Simpai %s " % str(ex))
            result.update({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error while parsing JOB from Simpai ",
                "error": "Exception is :" + str(ex)
            })
            return result
