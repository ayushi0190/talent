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
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_304_NOT_MODIFIED, HTTP_409_CONFLICT



from src.services.common.apis.resume_parser_services import ResumeParserServices
from src.services.common.apis.scorer_services import ScorerServices
from src.services.sovren.interfaces.parsers.resume_parser_interface import \
    ResumeParserInterface
from src.utilities.tasks import send_score, send_taltpool_response
from src.db.crud.sovren.submission_schema import SubmissionSchema
from src.services.sovren.helpers.misc_helpers import call_sovren_parse_resume, index_document
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.apis.job_parser_services import JobParserServices
from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from src.services.common.helpers.misc_helpers import create_resume_id, generate_resume_doc_id,\
                                                    generate_resume_md5,\
                                                    get_authorized_services
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.sovren.helpers.indexing_helper import resume_indexer
from src.services.sovren.apis.resume_parser_services import SovResumeParserServices
from src.services.sovren.interfaces.submission_interface import SubmissionInterface
from src.services.common.validations.job_parse_by_id_validations import JobParseByIdValidations
from src.services.common.validations.score_by_id_validations import ScoreByIdValidations
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema
from src.services.common.config.common_config import common_url_settings
from src.services.common.validations.parse_resume_validations import ParseResumeValidations
from src.services.common.apis.job_board_services import JobBoardServices
from src.services.sovren.helpers.misc_helpers import get_job_index


class SovSubmission(SubmissionInterface, ABC):
    """
    Submission
    """

    def __init__(self):
        self.parser = common_url_settings.get("SOVREN_SERVICE") #'sovren'
        self.resume_id = None
        self.index_id = None
        self.resume_document_id = None
        self.resume_md5 = None
        self.resume_parsed_resp = None
        self.score_parsed_resp = None
        self.send_to_talent_pool = True

    def call_submission(
            self, request,
            document_as_base_64_string: str, new_resume_info: dict,
            job_id: str,  name: str, first_name: str, last_name: str,
            email: str, phone: str, vendor: str,
            response_id: str, questions: list, score_required: str,
            api_source: str, additional_skills: list
    ) -> dict:
        """
        Parse resume with Sovren
        :param api_source: String
        :param score_required: String
        :param request:
        :param questions: List
        :param response_id: String
        :param vendor: String
        :param phone: String
        :param email: String
        :param last_name: String
        :param first_name: String
        :param name: String
        :param job_id: String
        :param document_as_base_64_string: String
        :return: dict
        """

        # Call Parse Job to validate whether its a valid Job ID or not
        # If valid then check, whether its parsed or not
        audit_model = AuditTrailsSchema()
        service_name = request.url.path
        job_parser = JobParserServices()
        job_parser.background = False
        #res_parser = SovResumeParserServices()
        res_parser = ResumeParserServices()
        res_parser.background = False
        score_services= ScorerServices()
        score_services.background = False
        save_sub = SubmissionSchema()
        result = {}
        source_job_url = ""
        job_board_api_source = ""
        # Get Client ID from HEADERS
        client_id = request.headers["client_id"]
        request.app.logger.info("Client ID for Submission %s " % client_id)

        job_board = JobBoardServices()

        # Check whether Job exist on JOB Board using Job_id
        request.app.logger.info("Job Id as Input to Job Board : %s" % job_id)
        job_details = job_board.check_job_exist(request, job_id)
        # If job NOT exist on JOB board
        # return message that JOBID does not exist on JOB Board
        if job_details.get("code") != HTTP_200_OK or \
                job_details.get("data", {}).get("status-code") != HTTP_200_OK:
            print('jobboard resp: {}'.format(job_details))
            # return job_details
            return dict({
                # 'code': job_details.get("data",{}).get("status-code", 500),
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                'message': "Job does not Exist on JobBoard",
                # "resp": job_details,
            })
        # If job exist on Job Board
        else:
            source_job_url = job_details.get("data"). \
                get("result")[0].get("job").get("source_job_url")

            request.app.logger.info("source_job_url : %s" % source_job_url)
            job_board_api_source  = job_details.get("data"). \
                get("result")[0].get("job").get("api_source")

            request.app.logger.info("job_board_api_source : %s" % job_board_api_source)

        job_data = {}
        job_data.update({
            "job_id": job_id,
            "parse_with": self.parser
        })
        job_obj = JobParseByIdValidations.parse_obj(job_data)
        request.app.logger.info("Type for Job Parse %s " % type(job_obj))
        job_info = job_parser.call_parse_job(request ,job_obj)
        request.app.logger.info("Parse Job from Submission : %s" % job_info.get("code"))
        request.app.logger.info('job_category: {}'.format(job_parser.job_category))

        if job_info.get("code") not in [HTTP_200_OK, HTTP_304_NOT_MODIFIED]:
            job_info.update({
                "Submission Message": "Submission Failed while parsing job: {}"
                        .format(job_info.get('messge'))
            })
            return job_info
        else:
            # Call Parse Resume to validate whether Resume is parsed or not
            res_data = {}
            res_data.update({
                "document_as_base_64_string": document_as_base_64_string,
                "additional_skills": additional_skills,
                "parse_with": self.parser
            })
            res_obj = ParseResumeValidations.parse_obj(res_data)
            request.app.logger.info("Type for Resume Parse %s " % type(res_obj))
            #resume_info = res_parser.parse_resume(request, document_as_base_64_string, background_task)
            if self.send_to_talent_pool:
                res_parser.send_to_talent_pool = True
            else:
                res_parser.send_to_talent_pool = False
            resume_info = res_parser.call_parse_resume(
                    request, res_obj,  new_resume_info)

            if resume_info.get("code") not in [HTTP_200_OK, HTTP_304_NOT_MODIFIED]:
                resume_info.update({
                    "Submission Message": "Submission Failed while parsing Resume: {}"
                        .format(resume_info.get('message'))
                })
                return resume_info

            else:
                self.resume_id = res_parser.resume_id
                self.resume_document_id = res_parser.resume_document_id
                self.index_id = res_parser.index_id
                self.resume_md5 = res_parser.resume_md5
                self.resume_parsed_resp = res_parser.resume_parsed_resp

                request.app.logger.info("Resume ID in Submission : %s" % self.resume_id)
                request.app.logger.info("Index ID ID in Submission : %s" % self.index_id)
                request.app.logger.info("Resume Document ID in Submission : %s" % self.resume_document_id)
                request.app.logger.info("Resume MD5 in Submission : %s" % self.resume_md5)
                #request.app.logger.info("Parsed Resume response in Submission : %s" % self.resume_parsed_resp)

                resume_info.update({
                    "resume_id": self.resume_id,
                    "resume_document_id": self.resume_document_id,
                    "resume_md5": self.resume_md5,
                    "index_id": self.index_id,
                    "resume_parsed_resp": self.resume_parsed_resp

                })
                # If job and resume parsed successfully then call score endpoint
                # Send score for the duplicate resume
                request.app.logger.info("Get Score ")
                score_data = {}
                score_data.update({
                    "job_id": job_id,
                    "resume_id": resume_info.get("resume_id"),
                    "job_category": job_parser.job_category,
                    "parse_with": self.parser
                })
                score_obj = ScoreByIdValidations.parse_obj(score_data)
                request.app.logger.info("Type for Score in Submission %s " % type(score_obj))

                score_info = score_services.call_get_score_by_id(request, score_obj)
                self.score_parsed_resp = score_services.score_parsed_resp

                if score_info.get("code") not in [HTTP_200_OK,HTTP_304_NOT_MODIFIED]:
                    score_info.update({
                        "Submission Message": "Submission Failed while Generating Score: {}"
                            .format(score_info.get('messge'))
                    })
                    return score_info
                else:
                    request.app.logger.info("Score Response received :  %s" % type(score_services.score_parsed_resp))

                    score_resp = json.loads(score_services.score_parsed_resp)
                    #request.app.logger.info("Score Response send for background task:  %s" % json.dumps(score_resp))
                    request.app.logger.info("Score Response send for background task:  %s" % type(score_resp) )
                    request.app.logger.info("Resume document ID: %s " % resume_info.get("resume_document_id"))

                    save_sub.add_submission(
                            request, resume_info.get("index_id"),
                            str(resume_info.get("resume_document_id")),
                            resume_info.get("resume_id"), job_id, client_id,
                            name, first_name, last_name, email, phone, vendor,
                            response_id, questions, score_required, 
                            api_source, self.parser)
                    request.app.logger.info("Save the submission request for sovren in DB ")
                    request.app.logger.info("Push Sovren score to HIRE")

                vms_input_data = {}
                job_db_id = job_id.split("-")
                request.app.logger.info("job_db_id: %s " % job_db_id[5])
                request.app.logger.info("parse_resume_status_code: %s " % resume_info.get("code"))
                vms_input_data.update({
                    "job_id" : job_db_id[5],
                    "phone" : phone,
                    "name" : name,
                    "first_name" : first_name,
                    "last_name" : last_name,
                    "email" : email,
                    "vendor" : vendor,
                    "question_answers" : questions,
                    "resume" : document_as_base_64_string,
                    "parse_resume_status_code" : resume_info.get("code"),
                    "response_id" : response_id


                })

                request.app.logger.info("Score input value in Submission : %s" % score_required)
                if common_url_settings.get("SOVREN_SERVICE") in score_required:
                    # Celery task to send score to SVMS or SimplifyHire
                    send_score.delay(score_resp, self.parser, response_id,
                                     job_id, resume_info.get("resume_id"), api_source, source_job_url, vms_input_data)
                else:
                    request.app.logger.info("Score not required for this submission")

                # Return submission response
                result.update({
                        "code": HTTP_200_OK,
                        "message": "Successful Submission",
                        "resume_code": resume_info.get("code"),
                        "resume_message": resume_info.get("message"),
                        "resume_id": resume_info.get("resume_id"),
                        "index_id": resume_info.get("index_id"),
                        "resume_document_id": str(resume_info.get("resume_document_id")),
                        "resume_md5": resume_info.get("resume_md5"),
                        "parsed_resume_resp": resume_info.get("resume_parsed_resp")
                        })
                audit_model.add(service_name,client_id)
                return result
        return result
    