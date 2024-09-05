# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Parser services
@author <rchakraborty@simplifyvms.com>
"""
import json
from typing import Dict
from datetime import datetime
import arrow
from fastapi import status
from pydantic import ValidationError
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from src.services.common.apis.job_board_services import JobBoardServices
from src.services.common.validations.job_parse_by_description_validations import JobParseByDescriptionValidations
from src.services.common.validations.submission_validations import SubmissionValidations
from src.services.sovren.apis.job_parser_services import SovJobParserServices
from src.services.sovren.apis.submission import SovSubmission
from src.services.sovren.helpers.indexing_helper import job_indexer, resume_indexer
from src.services.sovren.helpers.misc_helpers import get_job_index, format_job_description_request, \
    error_in_resume_doc_id
from src.services.common.helpers.misc_helpers import get_authorized_services
from src.services.simpai.apis.submission_services import SimpaiSubmission
from src.services.common.config.common_config import common_url_settings
from src.utilities.tasks import simpai_submission
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.helpers.misc_helpers import generate_resume_md5, check_and_create_resume_id
from src.services.common.helpers.pdf_helpers import append_to_pdf

class ParserServices:
    """
    Parser services class
    """
    def __init__(self):
        self.background = True
        self.send_to_talent_pool = True

    def call_get_parsed_job_by_id(self, request, data: dict) -> Dict:
        """
        Parse job
        :param request:
        :param data:
        :return:
        """
        service_info = get_authorized_services(request)

        try:
            # If Client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    sovren_parser = SovJobParserServices()
                    job_board = JobBoardServices()
                    job_details = job_board.check_job_existance(request, data.get("job_id"))
                    if job_details.get("code") != HTTP_204_NO_CONTENT:
                        job_index_id = get_job_index(data.get("job_id"))
                        job_indexer(request, job_index_id)
                        return sovren_parser.parse_job(request, data)
                    else:
                        return dict({
                            'code': HTTP_204_NO_CONTENT,
                            'message': "Job does not exists",
                            "data": {}
                        })
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

    def call_get_parsed_job_by_description(self, request, data: JobParseByDescriptionValidations) -> Dict:
        """
        Parse job
        :param request:
        :param data:
        :return:
        """
        service_info = get_authorized_services(request)

        try:
            # If Client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    sovren_parser = SovJobParserServices()
                    job_board = JobBoardServices()
                    result = sovren_parser.parse_with_job_board(
                        format_job_description_request(data)
                    )
                    if result.get("code") == HTTP_200_OK:
                        job_index_id = get_job_index(result.get("job_id"))
                        job_details = job_board.check_job_exist(request, result.get("job_id"))
                        return sovren_parser.parse_job(request, job_details, result.get("job_id"))
                    else:
                        return dict({
                            'code': HTTP_400_BAD_REQUEST,
                            'message': "Unable to parse job"
                        })
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

    def call_parse_submission(self, request, data: SubmissionValidations) -> Dict:
        """
        Parse job
        :param request:
        :param data:
        :return:
        """
        request.app.logger.info("===================== Submission Started ================")
        service_info = get_authorized_services(request)
        client_id = request.headers["client_id"]

        # Get resume index_id for client
        auth_schema = CltRegSchema()
        pool_info = auth_schema.get_client_info(request, client_id)
        index_id = pool_info.clt_res_idx_id
        request.app.logger.info("Index Id --> %s" % index_id)
        if not index_id:
            return dict({
                'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': "Resume index not found for client"
                })
        md5_hash = generate_resume_md5(data.document_as_base_64_string)
        request.app.logger.info("Md5 hash --> %s" % md5_hash)
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
            request.app.logger.info('orig_md5: {} \n new_md5: {} --> after additional skills'.format(md5_hash, new_md5_hash))
            #new_resume_info = check_and_create_resume_id(
            #        md5_hash, client_id, index_id, data.additional_skills)
            new_resume_info.update({'md5_hash': new_md5_hash})
        
        try:
            # If Client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov and data.parse_with.lower() \
                == common_url_settings.get("SOVREN_SERVICE"):
                    sovren_resume_parser = SovSubmission()
                    self.send_to_talent_pool = False
                    result = sovren_resume_parser.call_submission(
                            request, data.document_as_base_64_string, new_resume_info,
                            data.job_id, data.name, data.first_name,
                            data.last_name, data.email, data.phone, data.vendor,
                            data.response_id, data.questions, data.score_required,
                            data.api_source, data.additional_skills)
                    '''call simpai matcher in background '''
                    if common_url_settings.get("RUN_SIMPAI_IN_BACKGROUND") \
                    and self.background:
                        simpai_submission.delay(
                                client_id, data.document_as_base_64_string, new_resume_info,
                                data.job_id, data.name, data.first_name,
                                data.last_name, data.email, data.phone, data.vendor,
                                data.response_id, data.questions, data.score_required,
                                data.api_source, data.additional_skills)
                        pass
                    request.app.logger.info("===================== Submission End for Sovren ================")
                    return result
                # If selected tool is Opening
                if service_info.tol_ope and data.parse_with.lower() \
                == common_url_settings.get("OPENING_SERVICE"):
                    pass
                # If selected tool is Simplifyai
                if service_info.tol_sim and data.parse_with.lower() \
                == common_url_settings.get("SIMPAI_SERVICE"):
                    simpai_submission_obj = SimpaiSubmission()
                    self.send_to_talent_pool = False
                    result = simpai_submission_obj.call_submission(
                            client_id, data.document_as_base_64_string, new_resume_info,
                            data.job_id, data.name, data.first_name,
                            data.last_name, data.email, data.phone, data.vendor,
                            data.response_id, data.questions, data.score_required,
                            data.api_source, data.additional_skills)
                    return result
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



    def call_parse_resume_not_used(self, request, data: dict) -> Dict:
        """
        It will call Parse Resume based on the tool selected by client
        :param request:
        :param data: document_as_base_64_string
        :param data: index_id, Optional
        :return: JSON output
        """
        service_info = get_authorized_services(request)

        try:
            # If client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    sovren_resume_parser = SovrenResumeParserServices()
                    return sovren_resume_parser.parse_resume(request, data)
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

    def call_parse_job_not_used(self, request, data: dict) -> Dict:
        """
        It will call Parse JOB based on the tool selected by client
        :param request:

        :param data: job_id
        :return: JSON output
        """
        service_info = get_authorized_services(request)

        try:
            # If Client Info Exist
            if service_info:

                job_board = JobBoardServices()

                # Check whether Job exist on JOB Board using Job_id
                job_details = job_board.check_job_exist(request, data.get("job_id"))
                # If job NOT exist on JOB board
                # return message that JOBID does not exist on JOB Board
                if job_details.get("code") != HTTP_200_OK:
                    return job_details
                # If job exist on Job Board
                else:
                    # If selected tool is Sovren
                    if service_info.tol_sov:
                        sovren_job_parser = JobParserServices()
                        return sovren_job_parser.parse_job(request, data.dict())
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

    def call_delete_job(self, request, data: dict) -> Dict:
        """
        It will call Delete Job based on the index id and job id
        :param request:
        :param data: index_id
        :param data: job_id
        :return: JSON output
        """
        from src.services.sovren.helpers.misc_helpers import get_job_index
        service_info = get_authorized_services(request)
        job_index = get_job_index(data.job_id)
        try:
            # If client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    sovren_job_parser = SovJobParserServices()
                    return sovren_job_parser.delete_job(request, data.job_id,
                                                              data.delete_index, job_index)
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

    def call_delete_job_by_description(self, request, data: dict) -> Dict:
        """
        It will call Delete job based on Job description
        :param request:
        :param data: index_id
        :param data: job_id
        :return: JSON output
        """
        from src.services.sovren.helpers.misc_helpers import get_job_index
        service_info = get_authorized_services(request)
        job_index = get_job_index(data.job_id)
        try:
            # If client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    sovren_job_parser = SovJobParserServices()
                    return sovren_job_parser.delete_job(request, data.job_id,
                                                              data.delete_index, job_index)
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
