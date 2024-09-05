# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Job Parser services
@author <ankits@simplifyvms.com>
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
from src.services.common.validations.job_parse_by_id_validations import JobParseByIdValidations
from src.services.sovren.apis.job_parser_services import SovJobParserServices
from src.services.simpai.apis.job_parser_services import SimpJobParserServices
from src.services.sovren.helpers.indexing_helper import job_indexer, resume_indexer
from src.services.sovren.helpers.misc_helpers import get_job_index, format_job_description_request, \
    error_in_resume_doc_id
from src.services.sovren.helpers.resume_mapper_helpers import resume_mapper
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.helpers.misc_helpers import get_authorized_services
from src.services.common.config.common_config import common_url_settings
from src.utilities.tasks import parse_job_simpai
#from multiprocessing import Process

class JobParserServices:
    """
    Job Parser services class
    """

    def __init__(self):
        self.background = True
        self.job_category = None

    def call_parse_job(self, request, data: JobParseByIdValidations) -> Dict:
        """
        It will call Parse JOB based on the tool selected by client
        :param request:

        :param data: job_id
        :return: JSON output
        """
        service_info = get_authorized_services(request)
        client_id = request.headers["client_id"]

        try:
            # If Client Info Exist
            if service_info:

                job_board = JobBoardServices()

                # Check whether Job exist on JOB Board using Job_id
                request.app.logger.info("Job Id as Input to Job Board : %s" % data.job_id)
                job_details = job_board.check_job_exist(request, data.job_id)
                # If job NOT exist on JOB board
                # return message that JOBID does not exist on JOB Board
                if job_details.get("code") != HTTP_200_OK or \
                job_details.get("data",{}).get("status-code") != HTTP_200_OK:
                    print('jobboard resp: {}'.format(job_details))
                    #return job_details
                    return dict({
                        #'code': job_details.get("data",{}).get("status-code", 500),
                        "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'message': "Job does not Exist on JobBoard",
                        #"resp": job_details,
                    })
                # If job exist on Job Board
                else:
                    self.job_category = job_details.get("data"). \
                    get("result")[0].get("job").get("job_category")

                    # If selected tool is Sovren
                    if service_info.tol_sov and data.parse_with.lower() \
                    == common_url_settings.get("SOVREN_SERVICE"):
                        sovren_job_parser = SovJobParserServices()
                        result = sovren_job_parser.parse_job(request,job_details, data.job_id)
                        '''call simpai parser in background '''
                        if common_url_settings.get("RUN_SIMPAI_IN_BACKGROUND") \
                        and self.background:
                            parse_job_simpai.delay(client_id, job_details, data.job_id)
                        return result
                    # If selected tool is Opening
                    if service_info.tol_ope and data.parse_with.lower() \
                    == common_url_settings.get("OPENING_SERVICE"):
                        pass
                    # If selected tool is Simplifyai
                    if service_info.tol_sim and data.parse_with.lower() \
                    == common_url_settings.get("SIMPAI_SERVICE"):
                        simpai_job_parser = SimpJobParserServices()
                        result =  simpai_job_parser.parse_job(
                                client_id, job_details, data.job_id)
                        '''call test method in background
                        from src.utilities.background_task import Testing
                        obj = Testing()
                        prc = Process(target=obj.test, args=(request,'test-name2'))
                        prc.start()'''
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
