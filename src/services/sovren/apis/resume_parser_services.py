# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Resume parser services
@author <rchakraborty@simplifyvms.com>
"""
import json
from abc import ABC
from datetime import date
import arrow
import requests
from requests.exceptions import RequestException
import time

from src.db.crud.sovren.map_res_bkt_schema import MapResBktSchema
from src.db.crud.sovren.match_j_res_sc_schema import MatchJResScSchema
from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from src.db.crud.sovren.res_mapper_schema import ResMapperSchema
from src.services.sovren.apis.res_to_job_score_services import ResToJobScoreServices
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.common.config.common_config import common_url_settings
from src.services.sovren.helpers.indexing_helper import resume_indexer
from src.services.sovren.helpers.misc_helpers import (get_sovren_headers,
                                                      validate_resume_fields,
                                                      get_job_index,
                                                      data_to_save,
                                                      error_in_resume_doc_id,
                                                      error_parsing_resume,
                                                      duplicate_resume_error, index_document,
                                                      format_result_for_profile)
from src.services.sovren.helpers.resume_mapper_helpers import resume_mapper
from src.services.sovren.interfaces.parsers.resume_parser_interface import \
    ResumeParserInterface
from src.utilities.tasks import send_score, send_taltpool_response, parse_resume_simpai

from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_304_NOT_MODIFIED, HTTP_409_CONFLICT
from src.services.common.helpers.misc_helpers import create_resume_id, generate_resume_doc_id,\
                                                    generate_resume_md5
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.apis.job_parser_services import JobParserServices
from src.db.crud.sovren.intern_res_schema import InternResSchema
from datetime import datetime
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema

class SovResumeParserServices(ResumeParserInterface, ABC):
    """
    Resume parsing services
    """

    def __init__(self):
        self.parser = common_url_settings.get("SOVREN_SERVICE") #'sovren'
        self.resume_id = None
        self.index_id = None
        self.resume_document_id = None
        self.resume_md5 = None
        self.resume_parsed_resp = None
        self.send_to_talent_pool = True

    def parse_resume(self, request, document_as_base_64_string: str,
                     new_resume_info: dict, additional_skills: list):
        """
        If resume is already parsed then return it from DB
        Else Parse Resume from Sovren
        :param : request
        :param : resume_data
        :param : background_task
        :return: JSON output
        """
        auth_schema = CltRegSchema()
        resume_info = PrsResInfSchema()
        intern_resume = InternResSchema()
        audit_model = AuditTrailsSchema()
        service_name = request.url.path
        result = {}

        # Get Client ID from HEADERS
        client_id = request.headers["client_id"]

        # Create MD5 Hash with HEXDigest
        #md5_hash = generate_resume_md5(document_as_base_64_string)
        md5_hash = new_resume_info['md5_hash']
        request.app.logger.info("md5 hash : %s " % md5_hash)
        '''res_id, res_doc_id, index_id, md5_hash are passed as 
        dict param new_resume_info after checking DB'''
        orig_doc_md5 = new_resume_info['orig_doc_md5']
        index_id = new_resume_info['index_id']
        resume_doc_id = new_resume_info['resume_doc_id']
        resume_id = new_resume_info['resume_id']
        request.app.logger.info("document_as_base_64_string : %s " % len(document_as_base_64_string))

        # check md5_hash already existed or not in DB
        resume_parsed = resume_info.get_resume_info(request, md5_hash, client_id, self.parser)

        # If md5_hash already exist then get the parsed resume response from DB
        if resume_parsed:
            request.app.logger.info("Resume already parsed and saved in DB")
            if resume_parsed.doc_md5 == md5_hash:
                request.app.logger.info("MD5 HASH is same")

                # If the request is for same client the return the parsed response
                if resume_parsed.clt_id == client_id:
                    request.app.logger.info("Client ID is same")
                    self.resume_id = resume_parsed.res_id
                    self.index_id = resume_parsed.idx_id
                    self.resume_document_id = resume_parsed.res_doc_id
                    self.resume_md5 = resume_parsed.doc_md5
                    self.resume_parsed_resp = resume_parsed.resp

                    display_data = json.loads(resume_parsed.resp)
                    display_data = display_data.get('Value',{}).get('ParsedDocument','')
                    display_data = json.loads(display_data)

                    request.app.logger.info("Resume Id is %s and Index Id is %s " % (self.resume_id, self.index_id))
                    result.update({
                        'code': HTTP_304_NOT_MODIFIED,  # Need to add starllete response code for duplicate
                        'message': "Duplicate Resume",
                        'resume_id': resume_id,
                        'data': display_data,
                    })
                    if service_name != "/submission":
                        audit_model.add(service_name,client_id)
                    request.app.logger.info("Duplicate Resume for same client")
                    return result

                else:
                    # If it is not for same client
                    request.app.logger.info("Client ID is Different")
                    '''
                    pool_info = auth_schema.get_client_info(request, client_id)
                    index_id = ''
                    if pool_info.pol_prv:
                        index_id = pool_info.clt_res_idx_id
                    else:
                        index_id = data.index_id

                    request.app.logger.info("Index ID when it is for different client : %s" % index_id)
                    '''
                    #index_id = new_resume_info['index_id']

                    # Create Resume ID
                    #resume_id = new_resume_info['resume_id']
                    #resume_id = create_resume_id(index_id)
                    request.app.logger.info("Resume ID for already parsed Resume but for Different Client : %s"
                                            % resume_id)

                    self.resume_id = resume_id
                    self.index_id = index_id
                    self.resume_document_id = resume_parsed.res_doc_id
                    self.resume_md5 = resume_parsed.doc_md5
                    self.resume_parsed_resp = resume_parsed.resp

                    # Add parsed output in Sovren with new client's index id.
                    resume_index = resume_indexer(request, index_id)
                    if resume_index.get("code") != HTTP_200_OK:
                        return resume_index

                    # If Index exist
                    if resume_index.get("code") in [HTTP_200_OK]:

                        request.app.logger.info("Resume Index created for New client successfully")
                        prs_start_time = datetime.now()
                        client_index = index_document(request, resume_parsed.resp, index_id, \
                                                      resume_id, resume_parsed.res_doc_id)
                        prs_time_taken = (datetime.now()-prs_start_time).seconds
                        if client_index.get("code") != HTTP_200_OK:
                            return client_index

                        request.app.logger.info("Resume got Indexed for New client successfully")
                        formatted_result = {}
                        if index_id == common_url_settings.get("INTERNAL_BUCKET"):
                            data_to_save = intern_resume.add(
                                    request, index_id, resume_parsed.res_doc_id, resume_id,
                                    resume_parsed.resp, client_id, resume_parsed.doc_md5,
                                    document_as_base_64_string, prs_time_taken,
                                    self.parser, orig_doc_md5, additional_skills)
                        else:
                            data_to_save = resume_info.add(
                                    request, index_id, resume_parsed.res_doc_id,
                                    resume_id, resume_parsed.resp, client_id,
                                    resume_parsed.doc_md5, document_as_base_64_string, 
                                    prs_time_taken, self.parser, orig_doc_md5, additional_skills)

                        if data_to_save:
                            request.app.logger.info("Parsed got Indexed and Information Saved in DB ")
                            result.update({
                                "saved_in_DB": True
                            })
                        else:
                            request.app.logger.info("Parsed got Indexed but Information did not Saved in DB ")
                            result.update({
                                "saved_in_DB": False
                            })

                        if self.send_to_talent_pool:
                            request.app.logger.info("Resume already parsed and client is different then "
                                                    "call Background Task Celery")
                            send_taltpool_response.delay(HTTP_304_NOT_MODIFIED,"Duplicate Resume, added to new Index",
                                                         resume_id, index_id, resume_parsed.res_doc_id,
                                                         resume_parsed.resp, sovren_url_settings.get("SOVREN_SERVICE"), \
                                                         resume_parsed.doc_md5, client_id)

                        display_data = json.loads(resume_parsed.resp)
                        display_data = display_data.get('Value', {}).get('ParsedDocument', '')
                        display_data = json.loads(display_data)

                        formatted_result.update({
                            "code": HTTP_304_NOT_MODIFIED,
                            "message": "Duplicate Resume, added to new Index",
                            "resume_id": resume_id,
                            "data": display_data
                        })
                        if service_name != "/submission":
                            audit_model.add(service_name,client_id)

                        return formatted_result

        # If md5_hash not exist in DB then parse resume
        elif resume_parsed is None:
            request.app.logger.info("Resume not exist in DB and it has to be parse")
            '''
            pool_info = auth_schema.get_client_info(request, client_id)
            index_id = ''
            if pool_info.pol_prv:
                index_id = pool_info.clt_res_idx_id
            else:
                index_id = data.index_id

            request.app.logger.info("Index ID when it fresh resume got parsed : %s" % index_id)
            '''
            #index_id = new_resume_info['index_id']

            # Create resume document ID with HEXDigest
            #resume_doc_id = new_resume_info['resume_doc_id']
            #resume_doc_id = generate_resume_doc_id(document_as_base_64_string)
            request.app.logger.info("Resume Doc ID for New Resume : %s " % resume_doc_id)

            # Create Resume ID
            #resume_id = new_resume_info['resume_id']
            #resume_id = create_resume_id(index_id)
            request.app.logger.info("Resume ID for New Resume : %s" % resume_id)

            self.resume_id = resume_id
            self.index_id = index_id
            self.resume_document_id = resume_doc_id
            self.resume_md5 = md5_hash

            # Check Index ID exist or not
            resume_index = resume_indexer(request, index_id)

            if resume_index.get("code") != HTTP_200_OK:
                return resume_index

            # If Index exist
            if resume_index.get("code") in [HTTP_200_OK, HTTP_409_CONFLICT]:
                formatted_result = {}
                result = self.call_sovren_parse_resume(
                        request, document_as_base_64_string,
                        arrow.now().format('YYYY-MM-DD'), index_id,
                        resume_doc_id, resume_id, client_id, md5_hash,
                        orig_doc_md5,  additional_skills)

                if result.get("code") != HTTP_200_OK:
                    return result

                if result.get("code") == HTTP_200_OK:
                    self.resume_parsed_resp = result.get('data')

                    request.app.logger.info("send to talentpool : %s" % self.send_to_talent_pool)
                    if self.send_to_talent_pool:

                        send_taltpool_response.delay(
                                HTTP_200_OK, "Successfully Parse Resume",
                                resume_id, index_id, resume_doc_id, result.get('data'),
                                self.parser, md5_hash, client_id)

                    '''
                    if common_url_settings.get("RUN_SIMPAI_IN_BACKGROUND"):
                        parse_resume_simpai.delay(
                                resume_id, index_id, resume_doc_id, md5_hash, 
                                client_id, document_as_base_64_string, 
                                common_url_settings.get("SIMPAI_SERVICE"))
                        '''

                    display_data = json.loads(result.get('data'))
                    display_data = display_data.get('Value', {}).get('ParsedDocument', '')
                    display_data = json.loads(display_data)

                    formatted_result.update({
                        "code": result.get('code'),
                        "message": result.get('message'),
                        "resume_id": resume_id,
                        "data": display_data
                    })
                    if service_name != "/submission":
                        audit_model.add(service_name,client_id)

                    return formatted_result

    def call_sovren_parse_resume(self, request, base_64_encoded_string: str, revision_date: date,
                                 index_id: str, resume_document_id: str,
                                 resume_id: str, client_id: str, md5_hash: str,
                                 orig_doc_md5: str,
                                 additional_skills: list) -> dict:
        """
        Parse resume
        :param resume_id: String
        :param base_64_encoded_string: String
        :param revision_date: Date
        :param index_id: String
        :param resume_document_id: String
        :return:
        """
        prs_resume = PrsResInfSchema()
        intern_resume = InternResSchema()
        payload = {
            "DocumentAsBase64String": base_64_encoded_string,
            "IndexingOptions": {
                "IndexId": index_id,
                "DocumentId": resume_id,
            },
            "SkillsSettings" :  {
                                "Normalize" :  bool(True),
                                "TaxonomyVersion" :  "v2"
                                },
            "RevisionDate": revision_date,
        }
        calling_api = sovren_url_settings.get("SOVREN_PARSE_RESUME_URL")
        prs_start_time = datetime.now()
        start = time.time()
        result = self.connect_to_api(request, get_sovren_headers(), payload, \
                                     calling_api)
        prs_time_taken = (datetime.now()-prs_start_time).seconds
        if result.get("code") != HTTP_200_OK:
            return result

        # Save response to DB
        if result.get("code") == HTTP_200_OK:

            if index_id == common_url_settings.get("INTERNAL_BUCKET"):

                data_to_save = intern_resume.add(
                        request, index_id, str(resume_document_id), resume_id,
                         result.get('data'), client_id, md5_hash, 
                         base_64_encoded_string, prs_time_taken, self.parser,
                         orig_doc_md5, additional_skills)
            else:

                data_to_save = prs_resume.add(
                        request, index_id, str(resume_document_id), resume_id,
                        result.get('data'), client_id, md5_hash, 
                        base_64_encoded_string, prs_time_taken, self.parser,
                        orig_doc_md5, additional_skills)
            if data_to_save:
                request.app.logger.info("Parsed resume Saved in DB ")
                result.update({
                    "saved_in_DB": True
                })
            else:
                request.app.logger.info("Parsed resume NOT Saved in DB ")
                result.update({
                    "saved_in_DB": False
                })
            end = time.time()
            result = result
            request.app.logger.info("Resume Parser time taken for Sovren: %s " % (end - start))
            return result

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
            response = requests.request("POST", headers=header, \
                                        data=json.dumps(payload), url=calling_api)

            response_info = response.json()
            if response.status_code == HTTP_200_OK:
                result = {"code": response.status_code, \
                          'message': "Successfully Parse Resume", \
                          "data": json.dumps(response_info)}
            else:
                msg = response_info.get('Info', {}).get('Message','')
                result = {"code": response.status_code, \
                          "message": msg, \
                          "error": "Sovren unable to process the request"}
                request.app.logger.info("Sovren unable to proces the Resume request: " + str(msg))
            return result

        except Exception as ex:
            request.app.logger.info("Error while parsing Resume from Sovren %s " % str(ex))
            result.update({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error while parsing Resume from Sovren ",
                "error": "Exception is :" + str(ex)
            })
            return result

    def delete_resume(self, request, resume_id: str, index_deletion: bool, resume_index: str) -> dict:
        """
        If resume id exists in database
        Else revert back with undone message
        :param resume_index: String
        :param index_deletion: Bool
        :param request:
        :param resume_id: String
        :return: JSON output
        """
        auth_schema = CltRegSchema()
        resume_info = PrsResInfSchema()
        result = {}
        audit_model = AuditTrailsSchema()
        service_name = request.url.path

        # Get Client ID from HEADERS
        client_id = request.headers["client_id"]

        # Get resume
        resume = resume_info.get(resume_id)
        request.app.logger.info("Resume got : %s " % resume)

        # If resume id exists in database
        if resume is not None:
            # Call Sovren delete document operation
            deletion_result = self.connect_to_resume_deletion_api(request,
                                                                  get_sovren_headers(),
                                                                  resume_index,
                                                                  resume_id,
                                                                  sovren_url_settings.get("SOVREN_GET_INDEX_URL"))
            if deletion_result.get("code") == HTTP_200_OK:
                # Check if the request contains index_deletion to True
                if index_deletion:
                    index_deletion_result = self.connect_to_index_deletion_api(request,
                                                                               get_sovren_headers(),
                                                                               resume_index,
                                                                               sovren_url_settings.get(
                                                                                   "SOVREN_GET_INDEX_URL"))
                    if index_deletion_result.get("code") == HTTP_200_OK:
                        result.update({
                            "code": HTTP_200_OK,
                            "message": "Both resume and resume index deleted successfully",
                            "value": index_deletion_result.get("value")
                        })
                    else:
                        result.update({
                            "code": HTTP_500_INTERNAL_SERVER_ERROR,
                            "message": "Resume deleted successfully but unable to delete resume index",
                            "value": index_deletion_result.get("value")
                        })
                else:
                    result.update({
                        "code": HTTP_200_OK,
                        "message": "Resume deleted successfully",
                        "value": deletion_result.get("value")
                    })
                audit_model.add(service_name,client_id)
            else:
                result.update({
                    "code": HTTP_500_INTERNAL_SERVER_ERROR,
                    "message": "Unable to delete resume",
                    "value": None
                })

    def connect_to_resume_deletion_api(self, request, header: dict, resume_index: str, resume_id: str,
                                       calling_api: str) -> dict:
        """
        Delete resume by calling document deletion API of Sovren
        :param request:
        :param header:
        :param resume_index:
        :param resume_id:
        :param calling_api:
        :return:
        """
        extracted_data = {}
        deletion_api = calling_api + '/' + resume_index + '/documents/' + resume_id
        try:
            response = requests.request(
                "DELETE", headers=header, url=deletion_api
            )
            response_info = json.loads(json.dumps(response.json()))
            if response.status_code == HTTP_200_OK:
                # Set values in database before sending response here
                extracted_data.update({
                    'code': response.status_code,
                    'message': response_info['Info']['Message'],
                    'value': None,
                })
            else:
                extracted_data.update({
                    'code': response.status_code,
                    'message': response_info['Info']['Message'],
                    'value': None
                })

            return extracted_data
        except RequestException:
            pass

    def format_parse_profile(self, request, resume_status_code, resume_status_msg,
                             resume_id, index_id,
                             resume_document_id, resume_md5, parse_resp: dict):
        """

        """
        result = {}
        request.app.logger.info("Parsed type response from Sovren: %s" % type(parse_resp))

        input_data = json.loads(parse_resp)
        request.app.logger.info("Parsed type json after json loads: %s" % type(input_data))

        final_data = input_data.get('Value', {}).get('ParsedDocument', '')
        final_data = json.loads(final_data)
        request.app.logger.info("Parsed type json after one more time json loads: %s" % type(final_data))

        format_result = format_result_for_profile(request, final_data)

        result.update({
            "code": HTTP_200_OK,
            "message": "Parse profile for sovren",
            "resume_code": resume_status_code,
            "resume_message": resume_status_msg,
            "resume_id": resume_id,
            "index_id": index_id,
            "resume_document_id": str(resume_document_id),
            "resume_md5": resume_md5,
            "parsed_resume_resp": parse_resp,
            "formatted_response": format_result

        })
        return result




