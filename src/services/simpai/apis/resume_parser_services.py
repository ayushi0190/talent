# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Resume parser services
@author <ankits@simplifyvms.com>
"""

import json
from abc import ABC
from datetime import date
from wsgiref import headers
import arrow
import requests
from requests.exceptions import RequestException
from datetime import datetime
from fastapi import Request
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
                                                      )
from src.services.sovren.helpers.resume_mapper_helpers import resume_mapper
from src.services.sovren.interfaces.parsers.resume_parser_interface import \
    ResumeParserInterface
from src.utilities.tasks import send_score, send_taltpool_response, parse_resume_simpai

from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_304_NOT_MODIFIED, HTTP_409_CONFLICT
from src.services.common.helpers.misc_helpers import create_resume_id, generate_resume_doc_id, \
    generate_resume_md5
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.apis.job_parser_services import JobParserServices
from src.db.crud.sovren.intern_res_schema import InternResSchema

from src.services.simpai.helpers.misc_helpers import format_result_for_profile
from src.utilities.custom_logging import cust_logger as logger


class SimpaiResumeParserServices(ResumeParserInterface, ABC):
    """
    Resume parsing services
    """

    def __init__(self):
        self.parser = common_url_settings.get("SIMPAI_SERVICE")  # 'simplifyai'
        self.resume_id = None
        self.index_id = None
        self.resume_document_id = None
        self.resume_md5 = None
        self.resume_parsed_resp = None
        self.send_to_talent_pool = True
        pass

    def update_details(self, **kwargs):
        self.resume_id = kwargs.get('res_id')
        self.index_id = kwargs.get('index_id')
        self.resume_document_id = kwargs.get('res_doc_id')
        self.resume_md5 = kwargs.get('resume_md5')
        pass

    def parse_resume(self, client_id, document_as_base_64_string: str,
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
        result = {}
        request = None

        # Get Client ID from HEADERS
        # client_id = request.headers["client_id"]

        # Create MD5 Hash with HEXDigest
        # md5_hash = generate_resume_md5(document_as_base_64_string)
        md5_hash = new_resume_info['md5_hash']
        logger.info("md5 hash : %s " % md5_hash)
        '''res_id, res_doc_id, index_id, md5_hash are passed as 
        dict param new_resume_info after checking DB'''
        orig_doc_md5 = new_resume_info['orig_doc_md5']
        index_id = new_resume_info['index_id']
        resume_doc_id = new_resume_info['resume_doc_id']
        resume_id = new_resume_info['resume_id']

        # check md5_hash already existed or not in DB
        resume_parsed = resume_info.get_resume_info(request, md5_hash, client_id, self.parser)

        # If md5_hash already exist then get the parsed resume response from DB
        if resume_parsed:
            logger.info("Resume already parsed and saved in DB")
            if resume_parsed.doc_md5 == md5_hash:
                logger.info("MD5 HASH is same")

                # If the request is for same client the return the parsed response
                if resume_parsed.clt_id == client_id:
                    logger.info("Client ID is same")
                    self.resume_id = resume_parsed.res_id
                    self.index_id = resume_parsed.idx_id
                    self.resume_document_id = resume_parsed.res_doc_id
                    self.resume_md5 = resume_parsed.doc_md5
                    self.resume_parsed_resp = resume_parsed.resp

                    logger.info("parsed response type %s" % type(resume_parsed.resp))
                    display_data = json.loads(resume_parsed.resp)
                    logger.info("parsed response type1 %s" % type(display_data))
                    display_data = display_data.get('parsed_resume', {}).get('data', {})
                    # display_data = json.loads(display_data)

                    logger.info("Resume Id is %s and Index Id is %s " % (self.resume_id, self.index_id))
                    result.update({
                        'code': HTTP_304_NOT_MODIFIED,  # Need to add starllete response code for duplicate
                        'message': "Duplicate Resume",
                        'resume_id': resume_id,
                        'data': display_data
                    })
                    logger.info("Duplicate Resume for same client")
                    return result

                else:
                    # If it is not for same client
                    logger.info("Client ID is Different")
                    '''
                    pool_info = auth_schema.get_client_info(request, client_id)
                    index_id = ''
                    if pool_info.pol_prv:
                        index_id = pool_info.clt_res_idx_id
                    else:
                        index_id = data.index_id

                    logger.info("Index ID when it is for different client : %s" % index_id)
                    '''
                    # index_id = new_resume_info['index_id']

                    # Create Resume ID
                    # resume_id = new_resume_info['resume_id']
                    # resume_id = create_resume_id(index_id)
                    logger.info("Resume ID for already parsed Resume but for Different Client : %s"
                                % resume_id)

                    self.resume_id = resume_id
                    self.index_id = index_id
                    self.resume_document_id = resume_parsed.res_doc_id
                    self.resume_md5 = resume_parsed.doc_md5
                    self.resume_parsed_resp = resume_parsed.resp

                    # No need to create index in Sovren for Simpai request
                    # Add parsed output in Sovren with new client's index id.
                    # resume_index = resume_indexer(request, index_id)
                    resume_index = {"code": HTTP_200_OK}
                    if resume_index.get("code") != HTTP_200_OK:
                        return resume_index

                    # If Index exist
                    if resume_index.get("code") in [HTTP_200_OK]:

                        logger.info("Resume Index created for New client successfully")
                        prs_start_time = datetime.now()
                        ''' No need to index document in Sovren for Simpai
                        client_index = index_document(request, resume_parsed.resp, index_id, \
                                                      resume_id, resume_parsed.res_doc_id)
                        if client_index.get("code") != HTTP_200_OK:
                            return client_index
                        '''
                        prs_time_taken = (datetime.now() - prs_start_time).seconds

                        logger.info("Resume got Indexed for New client successfully")
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
                            logger.info("Parsed got Indexed and Information Saved in DB ")
                            result.update({
                                "saved_in_DB": True
                            })
                        else:
                            logger.info("Parsed got Indexed but Information did not Saved in DB ")
                            result.update({
                                "saved_in_DB": False
                            })

                        if self.send_to_talent_pool:
                            logger.info("Resume already parsed and client is different then "
                                        "call Background Task Celery")
                            send_taltpool_response.delay(
                                HTTP_304_NOT_MODIFIED, "Duplicate Resume, added to new Index",
                                resume_id, index_id, resume_parsed.res_doc_id,
                                resume_parsed.resp, self.parser, \
                                resume_parsed.doc_md5, client_id)

                        display_data = json.loads(resume_parsed.resp)
                        display_data = display_data.get('parsed_resume', {}).get('data', {})
                        # display_data = json.loads(display_data)

                        formatted_result.update({
                            "code": HTTP_304_NOT_MODIFIED,
                            "message": "Duplicate Resume, added to new Index",
                            "resume_id": resume_id,
                            "data": display_data
                        })

                        return formatted_result

        # If md5_hash not exist in DB then parse resume
        elif resume_parsed is None:
            logger.info("Resume not exist in DB and it has to be parse")
            '''
            pool_info = auth_schema.get_client_info(request, client_id)
            index_id = ''
            if pool_info.pol_prv:
                index_id = pool_info.clt_res_idx_id
            else:
                index_id = data.index_id

            logger.info("Index ID when it fresh resume got parsed : %s" % index_id)
            '''
            # index_id = new_resume_info['index_id']

            # Create resume document ID with HEXDigest
            # resume_doc_id = new_resume_info['resume_doc_id']
            # resume_doc_id = generate_resume_doc_id(document_as_base_64_string)
            logger.info("Resume Doc ID for New Resume : %s " % resume_doc_id)

            # Create Resume ID
            # resume_id = new_resume_info['resume_id']
            # resume_id = create_resume_id(index_id)
            logger.info("Resume ID for New Resume : %s" % resume_id)

            self.resume_id = resume_id
            self.index_id = index_id
            self.resume_document_id = resume_doc_id
            self.resume_md5 = md5_hash

            # Check Index ID exist or not
            # resume_index = resume_indexer(request, index_id)

            # if resume_index.get("code") != HTTP_200_OK:
            #    return resume_index

            # If Index exist
            # if resume_index.get("code") in [HTTP_200_OK, HTTP_409_CONFLICT]:
            formatted_result = {}
            result = self.call_simpai_parse_resume(
                request, document_as_base_64_string, index_id,
                resume_doc_id, resume_id, client_id, md5_hash,
                self.parser, orig_doc_md5, additional_skills)

            if result.get("code") != HTTP_200_OK:
                return result

            if result.get("code") == HTTP_200_OK:
                self.resume_parsed_resp = result.get('data')

                logger.info("send_to_talent_pool -- > %s " % self.send_to_talent_pool)
                if self.send_to_talent_pool:
                    logger.info("Resume parsed and call Background Task Celery")
                    send_taltpool_response.delay(
                        HTTP_200_OK, "Successfully parsed Resume",
                        resume_id, index_id, resume_doc_id,
                        result.get('data'), self.parser, \
                        md5_hash, client_id)

                display_data = json.loads(result.get('data'))
                logger.info("parsed response type1 %s" % type(display_data))
                display_data = display_data.get('parsed_resume', {}).get('data', {})
                # logger.info("Final response type %s " % type(display_data))
                formatted_result.update({
                    "code": result.get('code'),
                    "message": result.get('message'),
                    "resume_id": resume_id,
                    "data": display_data
                })

                return formatted_result

    def call_simpai_parse_resume(
            self, request: Request, base_64_encoded_string: str, index_id: str,
            resume_document_id: str, resume_id: str, client_id: str,
            md5_hash: str, parser_type: str, orig_doc_md5, additional_skills) -> dict:
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
        headers = {
            "Authorization": common_url_settings.get('SIMPAI_PARSER_AUTHORIZATION_KEY'),
            "Content-Type": 'application/json'
        }

        payload = {
            'base64_text': base_64_encoded_string
        }
        calling_api = common_url_settings.get("SIMPAI_PARSER_RESUME_URL")
        prs_start_time = datetime.now()
        start = time.time()
        result = self.connect_to_simpai_parse_resume_api(request, headers, payload, calling_api)

        prs_time_taken = (datetime.now() - prs_start_time).seconds

        if result.get("code") != HTTP_200_OK:
            return result

        # Save response to DB
        if result.get("code") == HTTP_200_OK:
            logger.info("Successfully got response for Parse Resume by SIMPAI")
            logger.info("SIMPAI Parsed response type : %s " % type(result.get('data')))
            # parse_resp = json.loads(result.get('data'))

            if index_id == common_url_settings.get("INTERNAL_BUCKET"):

                data_to_save = intern_resume.add(
                    request, index_id, str(resume_document_id), resume_id,
                    result.get('data'), client_id, md5_hash,
                    base_64_encoded_string, prs_time_taken, parser_type,
                    orig_doc_md5, additional_skills)
            else:
                # parse_resp.get('parsed_resume', {}).get('data', {})['education'] = norm_edu.get('data')
                data_to_save = prs_resume.add(
                    request, index_id, str(resume_document_id), resume_id,
                    result.get('data'), client_id, md5_hash, base_64_encoded_string,
                    prs_time_taken, parser_type, orig_doc_md5, additional_skills)

            if data_to_save:
                logger.info("Parsed resume Saved in DB ")
                result.update({
                    "saved_in_DB": True,
                })
            else:
                logger.info("Parsed resume NOT Saved in DB ")
                result.update({
                    "saved_in_DB": False,
                })
            result = result
            end = time.time()
            logger.info("Resume parser taken time for Simplifyai : %s " % (end - start))
            return result

    def connect_to_simpai_parse_resume_api(
            self, request: Request, header: dict, payload: dict,
            calling_api: str) -> dict:
        """
        Connect to SIMPAI API to parse resume
        :param header: Dictionary
        :param payload: Dictionary
        :param calling_api: String
        :return:
        """
        result = {}
        try:
            logger.info("call SIMPAI API for Parse Resume ")
            response = requests.request("POST", headers=header,
                                        data=json.dumps(payload), url=calling_api)
            logger.info("SIMPAI API status code for Parse Resume %s " % response.status_code)
            if response.status_code == HTTP_200_OK:

                response_info = response.json()
                result = {"code": response.status_code,
                          'message': "Successfully Parse Resume",
                          "data": json.dumps(response_info)}
            else:
                result = {"code": response.status_code,
                          "message": response.reason,
                          "error": "SIMPAI unable to parse the resume"}
                logger.info("SIMPAI unable to proces the Resume request ")
            return result

        except Exception as ex:
            logger.info("Error while parsing Resume from SIMPAI %s " % str(ex))
            result.update({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error while parsing Resume from SIMPAI ",
                "error": "Exception is :" + str(ex)
            })
            return result

    def format_parse_profile(self, request, resume_status_code, resume_status_msg,
                             resume_id, index_id,
                             resume_document_id, resume_md5, parse_resp: dict):
        """

        """
        result = {}
        logger.info("Parsed type response from SIMPAI: %s" % type(parse_resp))

        input_data = json.loads(parse_resp)
        logger.info("Parsed type json after json loads: %s" % type(input_data))

        final_data = input_data.get('parsed_resume', {}).get('data', {})
        # final_data = json.loads(final_data)
        # logger.info("Parsed type json after one more time json loads: %s" % type(final_data))

        format_result = format_result_for_profile(request, final_data)

        result.update({
            "code": HTTP_200_OK,
            "message": "Parse profile for simplifyai",
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
