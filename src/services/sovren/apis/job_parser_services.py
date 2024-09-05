# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Matching index services
@author <rchakraborty@simplifyvms.com>
"""
import json
import base64
from abc import ABC
import secrets
import arrow
import requests
from requests.exceptions import RequestException
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_409_CONFLICT, HTTP_304_NOT_MODIFIED
import time

#from src.db.crud.sovren.job_parser_schema import JobsToJobSchema
from src.db.crud.sovren.job_parser_schema import ParsedJobSchema
from src.services.common.apis.job_board_services import JobBoardServices
from src.db.crud.sovren.prs_jobs_inf_schema import PrsJobInfSchema
from src.db.crud.common.matching_index_schema import MatchingIndexSchema
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.config.common_config import common_url_settings
from src.services.common.helpers.misc_helpers import get_job_board_headers
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.sovren.helpers.indexing_helper import job_indexer
from src.services.sovren.helpers.misc_helpers import (get_sovren_headers,
                                                      serialize_job_ref, get_job_index)
from src.services.sovren.interfaces.parsers.job_parser_interface import \
    JobParserInterface
from datetime import datetime
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema

class SovJobParserServices(JobParserInterface, ABC):
    """
    Job board services
    """

    def __init__(self):
        self.job_parsed_resp = None
        self.parser = common_url_settings.get("SOVREN_SERVICE") #'sovren'

    def parse_with_job_board(self, data: dict) -> dict:
        """
        Parse job with job board
        :param data:
        :return:
        """
        secret_generator = secrets.SystemRandom()
        payload = {
            "source_job_id": secret_generator.randint(1, 100000),
            "source_id": "EX",
            "job_title": data.get("job_title"),
            "job_type": "Full Time",
            "job_category": "Others",
            "hire_type": "Full Time",
            "company_name": data.get("client_name"),
            "job_start_date": arrow.now().format("YYYY-MM-DD"),
            "job_description": data.get("job_description"),
            "publish_status": 1,
            "shift_start_time": "09:00",
            "shift_end_time": "17:00",
            "rate_type": "Weekly",
            "job_publish_date": arrow.now().format("YYYY-MM-DD HH:mm:ss"),
            "work_locations": data.get("work_locations"),
            "work_locations_ex": data.get("work_locations_ex")
        }
        return self.connect_to_job_board_api(get_job_board_headers(), payload,
                                             common_url_settings.get("JOB_BOARD_JOB_PARSING_URL"))

    def connect_to_job_board_api(self, header: dict, payload: dict,
                                 calling_api: str) -> dict:
        """
        Connect to job board for job parsing
        :param header:
        :param payload:
        :param calling_api:
        :return:
        """
        try:
            payload = json.dumps(payload)
            final_payload = payload.replace("\'s", "s")
            response = requests.request("POST", headers=header, data=final_payload, url=calling_api)
            response_info = json.loads(json.dumps(response.json()))
            if response.status_code == 200:
                response = {
                    "code": HTTP_200_OK,
                    "job_id": response_info.get("result").get("job_reference_number")
                }
            else:
                response = {
                    "code": HTTP_400_BAD_REQUEST,
                    "job_id": None
                }
            return response
        except Exception as ex:
            return dict({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error while processing job with job board ",
                "error": "Exception is :" + str(ex)
            })

    def parse_job(self, request, job_details, job_id: str ) -> dict:
        """
        It checks whether JOB parsed or not
        param : request
        param : job_details
        param data: job_id
        :return: JSON output
        """
        audit_model = AuditTrailsSchema()
        service_name = request.url.path
        job_schema = ParsedJobSchema()
        result = {}
        # Get Client ID from HEADERS
        client_id = request.headers["client_id"]

        parsed_job_info = job_schema.get_job_info(request, job_id, client_id, self.parser)

        # Check if JOB_ID already exist in DB or not
        # If Job_id EXISTS in DB return response from DB
        if parsed_job_info is not None:
            request.app.logger.info("JOB already exist in DB")

            display_data = json.loads(parsed_job_info.job_res)
            display_data = display_data.get('Value', {}).get('ParsedDocument', '')
            display_data = json.loads(display_data)

            result.update({
               'code': HTTP_304_NOT_MODIFIED,
               'message': "Duplicate JOB",
               'data': display_data
            })
            if service_name in ['/parse/job/by/id','/parse​/job​/by​/description'] :
                audit_model.add(service_name,client_id)
            return result
        else:
            # If Job_id does not Exists in DB
            request.app.logger.info("JOB does not exist in DB and need to Parse")
            job_description_base64 = job_details.get("data").get("result")[0].\
                get("job").get("job_description_base64")

            # decode base64

            job_description_bytes = base64.b64decode(job_description_base64)
            job_description_text = job_description_bytes.decode('utf-8')
            request.app.logger.info("Decoded JOB base64 type : %s and value %s " % (type(job_description_text), job_description_text[0:50]))


            job_title = job_details.get("data").get("result")[0]. \
                get("job").get("job_title")

            job_title = "\033[1m" + "Job Title: " + job_title + "\033[0m"


            job_location = job_details.get("data").get("result")[0]. \
                get("job").get("job_location")

            job_location = "\033[1m" + "Job Location: " + job_location + "\033[0m"

            job_text = job_title + '\n' + job_location + '\n' + job_description_text
            request.app.logger.info("Final JOB text : %s " % job_text[0:100])

            job_text_bytes = job_text.encode('utf-8')
            job_text_bytes = base64.b64encode(job_text_bytes)
            job_text = job_text_bytes.decode('utf-8')
            request.app.logger.info("Updated JOB base64 type  : %s  and its Value is : %s" % (type(job_text), job_text[0:50]))

            # Get the Job Index_id based on job_id
            job_index_id = get_job_index(job_id)
            request.app.logger.info("JOB index ID from get_job_index %s " % job_index_id)

            # Check Job Index ID exist or not
            job_index = job_indexer(request,job_index_id)

            # If Index returns success or it is already created
            # Call Parse Job
            if job_index.get("code") in [HTTP_200_OK, HTTP_409_CONFLICT]:
                result = self.sovren_parse_job(request,job_text, job_index_id,
                                               job_id, client_id )
                return result
            else:
                # If job_index returns some error while creating an index
                return job_index

    def sovren_parse_job(
            self, request, job_document: str, job_index_id: str, job_document_id: str, clt_id: str
    ) -> dict:
        """
        Parse job with Sovren
        :param job_document_id: String
        :param job_index_id: String
        :param job_document: String
        :return:
        """
        clt_id = request.headers['client_id']
        audit_model = AuditTrailsSchema()
        service_name = request.url.path
        job_parser = ParsedJobSchema()
        base_64_encoded_string = job_document
        revision_date = arrow.now().format("YYYY-MM-DD")
        index_id = job_index_id
        document_id = job_document_id

        payload = {
            "DocumentAsBase64String": base_64_encoded_string,
            "IndexingOptions": {
                "IndexId": index_id,
                "DocumentId": document_id,
            },
            "SkillsSettings" :  {
                                "Normalize" :  bool(True),
                                "TaxonomyVersion" :  "v2"
                                },
            "RevisionDate": revision_date,
        }
        prs_start_time = datetime.now()
        start = time.time()
        result = self.connect_to_api(request, get_sovren_headers(), payload,
                                     sovren_url_settings.get("SOVREN_PARSE_JOB_ORDER_URL") )
        prs_time_taken = (datetime.now()-prs_start_time).seconds
        if result.get("code") != HTTP_200_OK:
            return result

        # If a response from Sovren is 200
        if result.get("code") == HTTP_200_OK:
            formatted_result = {}
            data_to_save = job_parser.save_job(request, index_id, job_document_id,
                                               result.get('data'), clt_id, 
                                               self.parser, prs_time_taken)

            if data_to_save:
                request.app.logger.info("Parsed JOB Saved in DB ")
                result.update({
                    "saved_in_DB": True
                })
            else:
                request.app.logger.info("Parsed JOB NOT Saved in DB ")
                result.update({
                    "saved_in_DB": False
                })

            display_data = json.loads(result.get('data'))
            display_data = display_data.get('Value', {}).get('ParsedDocument', '')
            display_data = json.loads(display_data)

            formatted_result.update({
                "code": result.get('code'),
                "message": result.get('message'),
                "data": display_data
            })

            if service_name in ['/parse/job/by/id','/parse​/job​/by​/description'] :
                audit_model.add(service_name,clt_id)
            result = formatted_result
            end = time.time()
            request.app.logger.info("Job Parser time taken for Sovren: %s " % (end - start))
            return formatted_result

    def connect_to_api(self, request, header: dict, payload: dict,
                       calling_api: str) -> dict:
        """
        Connect to Sovren API to parse job
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
            response_info = response.json()
            if response.status_code == 200:

                result = {"code": HTTP_200_OK,
                          "message": "Successfully parsed the JOB",
                          "data": json.dumps(response_info)}
                request.app.logger.info("Successfully parsed the JOB ")
            else:
                msg = response_info.get('Info', {}).get('Message','')
                result = {"code": response.status_code, \
                          "message": msg, \
                          "error": "Sovren unable to process the Parse Job request"}
                request.app.logger.info("Sovren unable to process the Parse JOB request: " + str(msg))
            return result
        except Exception as ex:
            request.app.logger.info("Error while parsing JOB from Sovren %s " % str(ex))
            result.update({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error while parsing JOB from Sovren ",
                "error": "Exception is :" + str(ex)
            })
            return result

    def delete_job(self, request, job_id: str, index_deletion: bool, job_index: str) -> dict:
        """
        If job id exists in database
        Else revert back with undone message
        :param job_index: String
        :param index_deletion: Bool
        :param request:
        :param job_id: String
        :return: JSON output
        """
        auth_schema = CltRegSchema()
        job_info = PrsJobInfSchema()
        mat_index_schema = MatchingIndexSchema()
        result = {}
        audit_model = AuditTrailsSchema()
        service_name = request.url.path

        # Get Client ID from HEADERS
        client_id = request.headers["client_id"]

        # Get job
        job = job_info.get(job_id)
        request.app.logger.info("Job got : %s " % job)
        # If job id exists in database
        if job is not None:
            # Call Sovren delete document operation
            deletion_result = self.connect_to_job_deletion_api(request,
                                                                  get_sovren_headers(),
                                                                  job_index,
                                                                  job_id,
                                                                  sovren_url_settings.get("SOVREN_GET_INDEX_URL"))
            if deletion_result.get("code") == HTTP_200_OK:
                # Check if the request contains index_deletion to True
                index_deletion_result = self.connect_to_index_deletion_api(request,
                                                                           get_sovren_headers(),
                                                                           job_index,
                                                                           sovren_url_settings.get(
                                                                               "SOVREN_GET_INDEX_URL"))
                if index_deletion_result.get("code") == HTTP_200_OK:
                    result.update({
                        "code": HTTP_200_OK,
                        "message": "Both job and job index deleted successfully",
                        "value": index_deletion_result.get("value")
                    })
                else:
                    result.update({
                        "code": index_deletion_result['code'],
                        "message": index_deletion_result['message'],
                        "error": index_deletion_result['error']
                    })
                job_info.delete_job(job_id)
                mat_index_schema.delete_index(job_index)
                audit_model.add(service_name,client_id)
            else:
                result.update({
                    "code": deletion_result['code'],
                    "message": deletion_result['message'],
                    "error": deletion_result['error']
                })
        return result


    def connect_to_job_deletion_api(self, request, header: dict, document_index: str, document_id: str,
                                       calling_api: str) -> dict:
        """
        Delete job by calling document deletion API of Sovren
        :param request:
        :param header:
        :param job_index:
        :param job_id:
        :param calling_api:
        :return:
        """
        deletion_api = calling_api + '/' + document_index + '/documents/' + document_id
        try:
            response = requests.request(
                "DELETE", headers=header, url=deletion_api
            )

            if response.status_code == HTTP_200_OK:
                response_info = json.loads(json.dumps(response.json()))
                request.app.logger.info("Successfully deleted the document id from job board ")
                return dict({
                    'code': response.status_code,
                    'message': response_info['Info']['Message'],
                    'data': response_info['Value']
                })
            else:
                return dict({"code": response.status_code,
                             "message": response.reason,
                             "error": "Sovren unable to process the request"})
                request.app.logger.info("Sovren unable to proces the document id ")

        except Exception as ex:
            request.app.logger.info("Error while deleting JOB from Sovren %s " % str(ex))
            return dict({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error while deleting JOB from Sovren ",
                "error": "Exception is :" + str(ex)
            })
