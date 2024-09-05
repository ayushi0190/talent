# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Resume Parser services
@author <ankits@simplifyvms.com>
"""
from typing import Dict

from fastapi import status
from pydantic import ValidationError
from starlette.status import HTTP_200_OK, HTTP_304_NOT_MODIFIED

from src.services.common.helpers.misc_helpers import get_authorized_services
from src.services.sovren.apis.resume_parser_services import SovResumeParserServices
from src.services.common.config.common_config import common_url_settings
from src.services.simpai.apis.resume_parser_services import SimpaiResumeParserServices
from src.services.common.validations.parse_resume_validations import ParseResumeValidations
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.helpers.misc_helpers import generate_resume_md5, check_and_create_resume_id
from src.utilities.tasks import parse_resume_simpai_new
from src.services.common.helpers.pdf_helpers import append_to_pdf

class ResumeParserServices:
    """
    Resume Parser services class
    """

    def __init__(self):
        self.background = True
        self.resume_id = None
        self.index_id = None
        self.resume_document_id = None
        self.resume_md5 = None
        self.resume_parsed_resp = None
        self.send_to_talent_pool = True

    def call_parse_resume(self, request, data: ParseResumeValidations,
                           new_resume_info=None) -> Dict:
        """
        It will call Parse Resume based on the tool selected by client
        :param : request
        :param : data
        :param : background_task
        :return: JSON output
        """
        service_info = get_authorized_services(request)
        client_id = request.headers["client_id"]
        # Get resume index_id for client
        auth_schema = CltRegSchema()
        pool_info = auth_schema.get_client_info(request, client_id)
        index_id = pool_info.clt_res_idx_id
        if not index_id:
            return dict({
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': "Resume index not found for client"
                })
        md5_hash = generate_resume_md5(data.document_as_base_64_string)
        if not new_resume_info:
            if not data.additional_skills:
                '''Create common resume_doc_id, resume_id'''
                new_resume_info = check_and_create_resume_id(
                        md5_hash, client_id, index_id, md5_hash, None)
            else:
                # Check if orig_doc_m5 and additional skills are already parsed
                new_resume_info = check_and_create_resume_id(
                        None, client_id, index_id, md5_hash, data.additional_skills)
                if new_resume_info.get('md5_hash'):
                    new_doc_base64_str = new_resume_info.pop('doc_base64')
                    new_md5_hash = new_resume_info.get('md5_hash')
                else:
                    result = append_to_pdf(data.document_as_base_64_string,
                                           data.additional_skills)
                    if result.get('code') != HTTP_200_OK:
                        return result
                    new_doc_base64_str = result['data']
                    new_md5_hash = generate_resume_md5(new_doc_base64_str)
                print('base64', type(new_doc_base64_str), type(data.document_as_base_64_string))
                data.document_as_base_64_string = new_doc_base64_str
                print('orig_md5: {} \n new_md5: {}'.format(md5_hash, new_md5_hash))
                #new_resume_info = check_and_create_resume_id(
                #        md5_hash, client_id, index_id, data.additional_skills)
                new_resume_info.update({'md5_hash': new_md5_hash})

        try:
            # If client Info Exist
            if service_info:
                # If selected tool is Sovren
                '''call simpai matcher in background '''
                if service_info.tol_sov and data.parse_with.lower() \
                        == common_url_settings.get("SOVREN_SERVICE"):
                    if common_url_settings.get("RUN_SIMPAI_IN_BACKGROUND") \
                    and self.background:
                        parse_resume_simpai_new.delay(
                                client_id, data.document_as_base_64_string,
                                self.send_to_talent_pool, new_resume_info, data.additional_skills)
                        pass

                    sovren_resume_parser = SovResumeParserServices()
                    if self.background:
                        sovren_resume_parser.send_to_talent_pool = True
                    else:
                        sovren_resume_parser.send_to_talent_pool = False

                    result = sovren_resume_parser.parse_resume(
                            request, data.document_as_base_64_string
                            , new_resume_info, data.additional_skills)
                    self.resume_id = sovren_resume_parser.resume_id
                    self.index_id = sovren_resume_parser.index_id
                    self.resume_document_id = sovren_resume_parser.resume_document_id
                    self.resume_md5 = sovren_resume_parser.resume_md5
                    self.resume_parsed_resp = sovren_resume_parser.resume_parsed_resp
                    return result
                # If selected tool is Opening
                if service_info.tol_ope and data.parse_with.lower() \
                    == common_url_settings.get("OPENING_SERVICE"):
                    pass
                # If selected tool is Simplifyai
                if service_info.tol_sim and data.parse_with.lower() \
                    == common_url_settings.get("SIMPAI_SERVICE"):
                    simpai_resume_parser = SimpaiResumeParserServices()
                    simpai_resume_parser.send_to_talent_pool = True
                    result = simpai_resume_parser.parse_resume(
                            client_id, data.document_as_base_64_string,
                             new_resume_info, data.additional_skills)
                    self.resume_id = simpai_resume_parser.resume_id
                    self.index_id = simpai_resume_parser.index_id
                    self.resume_document_id = simpai_resume_parser.resume_document_id
                    self.resume_md5 = simpai_resume_parser.resume_md5
                    self.resume_parsed_resp = simpai_resume_parser.resume_parsed_resp
                    return result
            else:
                return dict({
                    'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'message': "No Client Information Exist"
                })

        except ValidationError as exc:
            return dict({
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': exc.errors()
            })

    def call_delete_resume(self, request, data: dict) -> Dict:
        """
        It will call Delete Resume based on the index id and resume id
        :param request:
        :param data: index_id
        :param data: resume_id
        :return: JSON output
        """
        service_info = get_authorized_services(request)

        try:
            # If client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    sovren_resume_parser = SovResumeParserServices()
                    return sovren_resume_parser.delete_resume(request, data.resume_id,
                                                              data.delete_index, service_info.clt_res_idx_id)
                # If selected tool is Opening
                if service_info.tol_ope:
                    pass
                # If selected tool is Simplifyai
                if service_info.tol_sim:
                    pass
            else:
                return dict({
                    'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'message': "No Client Information Exist"
                })

        except ValidationError as exc:
            return dict({
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': exc.errors()
            })

    def call_parse_profile(self, request, input_data, new_resume_info=None) -> Dict:
        """
        It will call Parse Resume based on the tool selected by client
        :param request:
        :param data: document_as_base_64_string
        :return: JSON output
        """
        service_info = get_authorized_services(request)
        client_id = request.headers["client_id"]
        # Get resume index_id for client
        auth_schema = CltRegSchema()
        pool_info = auth_schema.get_client_info(request, client_id)
        index_id = pool_info.clt_res_idx_id
        if not index_id:
            return dict({
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': "Resume index not found for client"
                })
        md5_hash = generate_resume_md5(input_data.document_as_base_64_string)
        if not new_resume_info:
            '''Create common resume_doc_id, resume_id'''
            new_resume_info = check_and_create_resume_id(
                    md5_hash, client_id, index_id, md5_hash, None)

        request.app.logger.info("parse_with for parse profile is : %s " % input_data.parse_with.lower())
        try:
            # If client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov and input_data.parse_with.lower() == common_url_settings.get("SOVREN_SERVICE"):
                    sovren_resume_parser = SovResumeParserServices()
                    sovren_resume_parser.send_to_talent_pool = False
                    #self.send_to_talent_pool = False
                    result = sovren_resume_parser.parse_resume(
                            request, input_data.document_as_base_64_string,
                             new_resume_info, None)
                    if result.get("code") in [HTTP_200_OK, HTTP_304_NOT_MODIFIED]:
                        self.resume_id = sovren_resume_parser.resume_id
                        self.index_id = sovren_resume_parser.index_id
                        self.resume_document_id = sovren_resume_parser.resume_document_id
                        self.resume_md5 = sovren_resume_parser.resume_md5
                        self.resume_parsed_resp = sovren_resume_parser.resume_parsed_resp
                        request.app.logger.info("ResumeID for parse profile : %s " % self.resume_id)
                        request.app.logger.info("index_id for parse profile : %s " % self.index_id)
                        request.app.logger.info("resume_document_id for parse profile : %s "
                                                % self.resume_document_id)
                        request.app.logger.info("resume_md5 for parse profile : %s " % self.resume_md5)
                        #request.app.logger.info("Parsed resume response for parse profile : %s "
                        #                        % self.resume_parsed_resp)
                        formatted_result = sovren_resume_parser. \
                            format_parse_profile(request, result.get("code"),
                                                 result.get("message"),
                                                 self.resume_id, self.index_id,
                                                 self.resume_document_id,
                                                 self.resume_md5, self.resume_parsed_resp)
                        return formatted_result
                    else:
                        return result

                # If selected tool is Opening
                if service_info.tol_ope and input_data.parse_with.lower() \
                    == common_url_settings.get("OPENING_SERVICE"):
                    pass
                # If selected tool is Simplifyai
                if service_info.tol_sim and input_data.parse_with.lower() == common_url_settings.get("SIMPAI_SERVICE"):
                    simpai_resume_parser = SimpaiResumeParserServices()
                    simpai_resume_parser.send_to_talent_pool = False
                    #self.send_to_talent_pool = False
                    result = simpai_resume_parser.parse_resume(
                            client_id, input_data.document_as_base_64_string,
                             new_resume_info, None)
                    if result.get("code") in [HTTP_200_OK, HTTP_304_NOT_MODIFIED]:
                        self.resume_id = simpai_resume_parser.resume_id
                        self.index_id = simpai_resume_parser.index_id
                        self.resume_document_id = simpai_resume_parser.resume_document_id
                        self.resume_md5 = simpai_resume_parser.resume_md5
                        self.resume_parsed_resp = simpai_resume_parser.resume_parsed_resp
                        request.app.logger.info("ResumeID for parse profile : %s " % self.resume_id)
                        request.app.logger.info("index_id for parse profile : %s " % self.index_id)
                        request.app.logger.info("resume_document_id for parse profile : %s "
                                                % self.resume_document_id)
                        request.app.logger.info("resume_md5 for parse profile : %s " % self.resume_md5)
                        #request.app.logger.info("Parsed resume response for parse profile : %s "
                        #                        % self.resume_parsed_resp)
                        formatted_result = simpai_resume_parser. \
                            format_parse_profile(request, result.get("code"),
                                                 result.get("message"),
                                                 self.resume_id, self.index_id,
                                                 self.resume_document_id,
                                                 self.resume_md5, self.resume_parsed_resp)
                        return formatted_result
                    else:
                        return result

            else:
                return dict({
                    'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'message': "No Client Information Exist"
                })

        except ValidationError as exc:
            return dict({
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': exc.errors()
            })

