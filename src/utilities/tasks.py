# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Celery task to push the score to client
@author <Ankits@simplifyvms.com>
"""
from urllib import response
from fastapi import APIRouter, Request as request

from datetime import datetime
import requests
import json
import sys
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_304_NOT_MODIFIED
from faker import Faker

from src.services.common.config import common_config
from src.db.crud.sovren.cel_que_log_schema import CeleryQueLogSchema
from src.services.common.helpers import misc_helpers
from src.utilities.celery import celery_app
from celery.utils.log import get_task_logger
from src.services.common.config.common_config import common_url_settings
from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from src.db.crud.sovren.intern_res_schema import InternResSchema
from src.utilities.celery_helpers import add_celery_task_log, update_celery_task_log
# from src.utilities.custom_logging import CustomizeLogger
# logger = CustomizeLogger.make_logger()

import logging

logger = get_task_logger(__name__)
logger.setLevel(logging.INFO)


@celery_app.task(bind=True, name='svrn')
def send_score(self, score_response, parser_type, response_id, job_id, resume_id, api_source, source_job_url=None,
               vms_input_data=None):
    """

    """
    logger.info(f"Source_job_url %s" % source_job_url)
    logger.info(f"vms_iput_data  %s" % vms_input_data)
    logger.info(f"api_source %s" % api_source)
    logger.info("Enter in send_score background task for  %s: " % parser_type)

    result = False
    try:

        add_task_req = {}
        add_task_req.update({
            "res_id": resume_id,
            "job_id": job_id,
            "is_pros": False,
            "req_type": "submission",
            "clt_resp": "",
            "parser": parser_type
        })
        celery_sch = CeleryQueLogSchema()
        celery_sch.add_task(add_task_req)

        logger.info("Validate data in DB for Celery send_score %s" % type(score_response))

        '''This method is only for Hire format and Sovren JSON.
        Need to create new function for diff parser output and SVMS format.
        Need to decide which format is required'''
        def info_from_service(service, value):
            if not source_job_url and api_source:
                payload = misc_helpers.get_hire_score_format(data, value, parser_type)

                logger.info(f"Payload to send score for {service} %s" % payload)
                headers = {
                    'Authorization': common_config.common_url_settings. \
                        get('SIMPLIFY_HIRE_SUBMISSION_SCORE_AUTHORIZATION'),
                    'Content-Type': 'application/json'
                }
                # request_url = api_source + common_config.common_url_settings.get('SOVREN_SUBMISSION_SCORE_TO_HIRE')

                request_url = api_source
                logger.info("Request url for submission %s " % request_url)

                response = requests.request(
                    "POST", request_url, data=json.dumps(payload), headers=headers, timeout=50)

                logger.info("Response for send_score url %s " % response.json())

            elif source_job_url and api_source:
                logger.info("For VMS -- scenario 3 ")
                logger.info("source_job_url  in celery task  %s: " % source_job_url)
                logger.info("api_source  in celery task  %s: " % api_source)
                # logger.info("data  in celery task  %s: " % data)
                # logger.info("value  in celery task  %s: " % json.dumps(value))

                vms_payload = misc_helpers.get_vms_score_format(data, value, parser_type, vms_input_data)

                logger.info(f"VMS Payload to send score for {service} %s" % json.dumps(vms_payload))

                vms_headers = {
                    'X-Token': common_config.common_url_settings. \
                        get('SVMS_PUSH_SCORE_AUTHORIZATION'),
                    'Content-Type': 'application/json'
                }
                vms_request_url = source_job_url + common_config.common_url_settings.get('SVMS_PUSH_SCORE_URL')

                request_url = api_source
                logger.info("VMS Request url for submission %s " % vms_request_url)

                vms_response = requests.request(
                    "POST", vms_request_url, data=json.dumps(vms_payload), headers=vms_headers, timeout=50)

                logger.info("VMS Response for send_score url %s " % vms_response.text)

                payload = misc_helpers.get_hire_score_format(data, value, parser_type)

                logger.info(f"HIRE Payload to send score for {service} %s" % json.dumps(payload))
                headers = {
                    'Authorization': common_config.common_url_settings. \
                        get('SIMPLIFY_HIRE_SUBMISSION_SCORE_AUTHORIZATION'),
                    'Content-Type': 'application/json'
                }
                # request_url = api_source + common_config.common_url_settings.get('SOVREN_SUBMISSION_SCORE_TO_HIRE')

                logger.info("HIRE Request url for submission %s " % request_url)

                response = requests.request(
                    "POST", request_url, data=json.dumps(payload), headers=headers, timeout=50)

                logger.info("HIRE Response for send_score url %s " % response.text)
            return payload, response

        if parser_type == common_url_settings.get('SOVREN_SERVICE'):
            value = score_response.get("Value", {})
            matches = value.get("Matches", [])
            if len(matches) == 0:
                data = {}
            else:
                data = matches[0]

            data.update({
                'resume_id': resume_id,
                'response_id': response_id,
                'job_reference_number': job_id
            })
            payload, response = info_from_service('sovren', value)

            # if api_source is not null and source_job_url is not null:

        elif parser_type == common_url_settings.get('SIMPAI_SERVICE'):
            value = score_response.get("Value", {})
            matches = value.get("Matches", [])
            if len(matches) == 0:
                data = {}
            else:
                data = matches[0]
            data.update({
                'resume_id': resume_id,
                'response_id': response_id,
                'job_reference_number': job_id
            })
            payload, response = info_from_service('simplifyai', value)
            
            logger.info("Payload to send score for simpai %s" % payload)
        # result = False
        else:
            logger.error("No need to send score for parser: {}".format(parser_type))
            result = False
            return result

        # Update DB status score pushed to Client
        data = {}
        data.update({
            "job_id": job_id,
            "res_id": resume_id,
            "req_type": "submission",
            "parser": parser_type
        })
        if response.status_code == HTTP_200_OK:
            data.update({
                "clt_resp": json.dumps(response.json()),
                "is_pros": True
            })
            result = True
        else:
            data.update({
                "clt_resp": response.text,
                "is_pros": False
            })
            result = False

        celery_sch.update(data)
        logger.info("Update data in DB for send_score ")
    except Exception as ex:
        logger.error("Error while sending score by Celery Task %s " % str(ex))
    return result


@celery_app.task(bind=True, name='talentpool')
def send_taltpool_response(self, resume_code, resume_message, res_id, index_id,
                           res_doc_id, res_response, service_name, md5_hash,
                           client_id):
    """
    Sending Final Response to TalentPool
    """
    result = False
    try:
        req_type = "talentpool_parse_resume"
        add_task_req = {}
        add_task_req.update({
            "res_id": res_id,
            "job_id": "job_id",
            "is_pros": False,
            "req_type": req_type,
            "clt_resp": ""
        })
        celery_sch = CeleryQueLogSchema()
        celery_sch.add_task(add_task_req)
        logger.info("Add data in DB for Celery send_taltpool_response ")

        talnt_pool_data = {}
        talnt_pool_data.update({
            "resume_code": resume_code,
            "resume_message": resume_message,
            "resume_document_id": str(res_doc_id),
            "resume_md5": md5_hash,
            "index_id": index_id,
            "resume_id": res_id,
            "client_id": client_id,
            "parsed_resume_doc": {
                service_name: json.dumps(res_response)
            },
            "service_name": [service_name],
        })

        request_url = common_config.common_url_settings.get("TALENTPOOL_UPDATE")
        logger.info("TalentPool Request url %s" % request_url)

        # logger.info("Talentpool payload for Parse Resume : %s " % json.dumps(talnt_pool_data))
        response = requests.request("POST", request_url,
                                    data=json.dumps(talnt_pool_data), timeout=50)
        data = {}
        data.update({
            "job_id": "job_id",
            "res_id": res_id,
            "req_type": req_type,
        })
        print("For Parse resume", response.json())
        logger.info("Response from Talentpool for parse resume : %s" % json.dumps(response.json()))

        if response.status_code == HTTP_200_OK:
            data.update({
                "clt_resp": json.dumps(response.json()),
                "is_pros": True
            })
            result = True
        else:
            data.update({
                "clt_resp": response.text,
                "is_pros": False
            })
            result = False
        celery_sch.update(data)
        logger.info("Update data in DB for send_taltpool_response ")
    except Exception as ex:
        logger.error("Error while sending response for Talentpool by Celery Task %s " % str(ex))
    return result


@celery_app.task(bind=True, name='talentpool_clt')
def send_clt_reg_taltpool(self, client_name, client_id):
    """
    Sending Client Register Response to TalentPool
    """
    fake = Faker()
    result = False
    try:
        res_id = "res_id" + str(fake.pyint())
        job_id = "job_id" + str(fake.pyint())
        add_task_req = {}
        add_task_req.update({
            "res_id": res_id,
            "job_id": job_id,
            "is_pros": False,
            "req_type": "clt_reg",
            "clt_resp": ""
        })
        celery_sch = CeleryQueLogSchema()
        celery_sch.add_task(add_task_req)
        logger.info("Add data in DB for Celery send_clt_reg_taltpool Client Register ")

        talnt_pool_data = {}
        talnt_pool_data.update({
            "client_name": str(client_name),
            "client_id": client_id
        })
        request_url = common_config.common_url_settings.get("TALENTPOOL_CLIENT_REGISTER")
        logger.info("TalentPool Request url for send_clt_reg_taltpool %s" % request_url)

        response = requests.request("POST", request_url, data=json.dumps(talnt_pool_data))
        data = {}
        data.update({
            "res_id": res_id,
            "job_id": job_id,
            "req_type": "clt_reg",
        })
        logger.info("Response from Talentpool for Register Client : %s" % json.dumps(response.json()))

        if response.status_code == HTTP_200_OK or HTTP_201_CREATED:
            data.update({
                "clt_resp": json.dumps(response.json()),
                "is_pros": True
            })
            result = True
        else:
            data.update({
                "clt_resp": json.dumps(response.json()),
                "is_pros": False
            })
            result = False
        celery_sch.update(data)
        logger.info("Update data in DB for Celery Client Register ")
    except Exception as ex:
        logger.error("Error while sending response to Talentpool by Celery Task %s " % str(ex))
    return result


@celery_app.task(bind=True, name='simpai_submission')
def simpai_submission(self, client_id, document_as_base_64_string: str, new_resume_info: dict,
                      job_id: str, name: str, first_name: str, last_name: str,
                      email: str, phone: str, vendor: str, response_id: str,
                      questions: list, score_required: str, api_source: str,
                      additional_skills: list):
    """
    Parse Job
    :param client_id: String
    :param data: object
    :param new_resume_info: String
    :return:
    """
    logger.info("===================== Submission Started for SIMPAI ================")
    from src.services.simpai.apis.submission_services import SimpaiSubmission
    parser_type = common_url_settings.get("SIMPAI_SERVICE")  # 'simplifyai'
    status = False
    try:
        req_type = 'submission'
        add_celery_task_log('', job_id, req_type, parser=parser_type)
        logger.info("Add data in DB for Celery simpai_submission")

        submission = SimpaiSubmission()
        submission.send_to_talent_pool = True
        response = submission.call_submission(
            client_id, document_as_base_64_string, new_resume_info,
            job_id, name, first_name, last_name, email, phone, vendor,
            response_id, questions, score_required, api_source,
            additional_skills)
        logger.info("Message from SIMPAI simpai_submission: {}".format(response.get('message')))

        resp = ''
        if response.get('code') in [HTTP_200_OK, HTTP_304_NOT_MODIFIED]:
            status = True
            resp = response.get('message')
        else:
            resp = response.get('message')
            status = False
        update_celery_task_log('', job_id, req_type, status, resp, parser=parser_type)
        logger.info("Update data in DB for Celery simpai_submission")
        logger.info("===================== Submission End for SIMPAI ================")
    except Exception as ex:
        logger.error("Error while submission from SIMPAI by Celery Task %s " % str(ex))
    return status


'''
1. Issue in passing request object to celery task - 
Error: fastapi kombu.exceptions.EncodeError: Object of type Request is not JSON serializable
2. Issue in passing resquest object to child process (Multiprocessing) - 
Error: AttributeError: Can't pickle local object 'FastAPI.setup.<locals>.openapi'
'''


@celery_app.task(bind=True, name='simpai_score_job_resume')
def score_job_resume_simpai(self, client_id: str, res_id: str, job_id: str, job_category: str):
    """
    Parse Job
    :param client_id: String
    :param job_id: String
    :param res_id: String
    :return:
    """
    from src.services.simpai.apis.scorer_services import SimpResToJobScoreServices
    parser_type = common_url_settings.get("SIMPAI_SERVICE")  # 'simplifyai'
    status = False
    try:
        req_type = 'score_job_resume'
        add_celery_task_log(res_id, job_id, req_type, parser=parser_type)
        logger.info("Add data in DB for Celery Score by SIMPAI")

        scorer = SimpResToJobScoreServices()
        response = scorer.get_score(client_id, res_id, job_id, job_category)
        logger.info("Message from SIMPAI score: {}".format(response.get('message')))

        resp = ''
        if response.get('code') in [HTTP_200_OK, HTTP_304_NOT_MODIFIED]:
            status = True
            resp = response.get('message')
        else:
            resp = response.get('message')
            status = False
        update_celery_task_log(res_id, job_id, req_type, status, resp, parser=parser_type)
        logger.info("Update data in DB for Celery Score")
    except Exception as ex:
        logger.error("Error while scoring from SIMPAI by Celery Task %s " % str(ex))
    return status


@celery_app.task(bind=True, name='simpai_parse_job')
def parse_job_simpai(self, client_id: str, job_details: str, job_id: str):
    """
    Parse Job
    :param client_id: String
    :param job_details: String
    :param job_id: String
    :return:
    """
    from src.services.simpai.apis.job_parser_services import SimpJobParserServices
    parser_type = common_url_settings.get("SIMPAI_SERVICE")  # 'simplifyai'
    status = False
    try:
        req_type = 'parse_job'
        add_celery_task_log('', job_id, req_type, parser=parser_type)
        logger.info("Add data in DB for Celery Parse Job by SIMPAI")

        parser = SimpJobParserServices()
        # response = parser.start_parse_job(None, client_id, job_details, job_id)
        response = parser.parse_job(client_id, job_details, job_id)
        logger.info("Message from SIMPAI parse job: {}".format(response.get('message')))

        resp = ''
        if response.get('code') in [HTTP_200_OK, HTTP_304_NOT_MODIFIED]:
            status = True
            resp = response.get('message')
        else:
            resp = response.get('message')
            status = False
        update_celery_task_log('', job_id, req_type, status, resp, parser=parser_type)
        logger.info("Update data in DB for Celery Job")
    except Exception as ex:
        logger.error("Error while parsing job from SIMPAI by Celery Task %s " % str(ex))
    return status


@celery_app.task(bind=True, name='simpai_parse_resume_new')
def parse_resume_simpai_new(self, client_id, document_as_base_64_string: str,
                            send_to_talent_pool: bool, new_resume_info: dict,
                            additional_skills: list):
    """
    Parse Job
    :param client_id: String
    :param res_id: String
    :param document_as_base_64_string: String
    :return:
    """
    from src.services.simpai.apis.resume_parser_services import SimpaiResumeParserServices
    parser_type = common_url_settings.get("SIMPAI_SERVICE")  # 'simplifyai'
    status = False
    try:
        res_id = new_resume_info['resume_id']
        req_type = 'parse_resume'
        add_celery_task_log(res_id, '', req_type, parser=parser_type)
        logger.info("Add data in DB for Celery Parse Job by SIMPAI")

        parser = SimpaiResumeParserServices()
        parser.send_to_talent_pool = True
        response = parser.parse_resume(client_id, document_as_base_64_string,
                                       new_resume_info, additional_skills)
        logger.info("Message from SIMPAI parse resume: {}".format(response.get('message')))

        resp = ''
        if response.get('code') in [HTTP_200_OK, HTTP_304_NOT_MODIFIED]:
            status = True
            resp = response.get('message')
        else:
            resp = response.get('message')
            status = False
        update_celery_task_log(res_id, '', req_type, status, resp, parser=parser_type)
        logger.info("Update data in DB for Celery Job")
    except Exception as ex:
        logger.error("Error while parsing job from SIMPAI by Celery Task %s " % str(ex))
    return status


@celery_app.task(bind=True, name='simpai_parse_resume')
def parse_resume_simpai(self, res_id, index_id, res_doc_id, md5_hash, client_id,
                        document_as_base_64_string, parser_type):
    """

    """
    result = False
    try:
        req_type = "parse_resume"
        add_task_req = {}
        add_task_req.update({
            "res_id": res_id,
            "job_id": "job_id",
            "is_pros": False,
            "req_type": req_type,
            "clt_resp": "",
            "parser": parser_type
        })
        celery_sch = CeleryQueLogSchema()
        celery_sch.add_task(add_task_req)
        logger.info("Add data in DB for Celery Parse Resume by SIMPAI")

        response = call_simpai_parse_resume(
            document_as_base_64_string, index_id,
            res_doc_id, res_id, client_id, md5_hash, parser_type)

        data = {}
        data.update({
            "job_id": "job_id",
            "res_id": res_id,
            "req_type": req_type,
            "parser": parser_type
        })
        # logger.info("Response from SIMPAI for parse resume : %s" % json.dumps(response.get('data')))
        logger.info("Message from SIMPAI parse resume: {}".format(response.get('message')))

        if response.get('code') == HTTP_200_OK:
            data.update({
                "clt_resp": response.get('message'),
                "is_pros": True,
            })
            result = True
        else:
            data.update({
                "clt_resp": response.get('message'),
                "is_pros": False,
            })
            result = False
        celery_sch.update(data)
        logger.info("Update data in DB for Celery Resume ")
    except Exception as ex:
        logger.error("Error while parsing resume from SIMPAI by Celery Task %s " % str(ex))
    return result


def call_simpai_parse_resume(base_64_encoded_string: str, index_id: str,
                             resume_document_id: str, resume_id: str, client_id: str, md5_hash: str,
                             parser_type: str) -> dict:
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
    result = connect_to_simpai_parse_resume_api(headers, payload, calling_api)
    prs_time_taken = (datetime.now() - prs_start_time).seconds
    if result.get("code") != HTTP_200_OK:
        return result

    # Save response to DB
    if result.get("code") == HTTP_200_OK:
        logger.info("Successfully got response for Parse Resume by SIMPAI")
        if index_id == common_url_settings.get("INTERNAL_BUCKET"):

            data_to_save = intern_resume.add(request, index_id, str(resume_document_id), resume_id,
                                             result.get('data'), client_id, md5_hash, base_64_encoded_string,
                                             prs_time_taken, parser_type)
        else:

            data_to_save = prs_resume.add(request, index_id, str(resume_document_id), resume_id,
                                          result.get('data'), client_id, md5_hash, '',
                                          prs_time_taken, parser_type)
        if data_to_save:
            logger.info("Parsed resume Saved in DB ")
            result.update({
                "saved_in_DB": True
            })
        else:
            logger.info("Parsed resume NOT Saved in DB ")
            result.update({
                "saved_in_DB": False
            })

        return result


def connect_to_simpai_parse_resume_api(header: dict, payload: dict, calling_api: str) -> dict:
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


