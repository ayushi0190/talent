# -*- coding: utf-8 -*-
import imp
import time
import json
from unittest import result
import requests

from src.services.common.config.common_config import common_url_settings
from src.services.simpai.config.simpai_config import simpai_url_settings
from src.services.sovren.interfaces.scorers.scorer_interface import ScorerInterface
from src.db.crud.sovren.match_j_res_sc_schema import MatchJResScSchema
from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from src.db.crud.sovren.prs_jobs_inf_schema import PrsJobInfSchema
from src.services.sovren.helpers.misc_helpers import (get_job_index, get_resume_index)
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_409_CONFLICT, HTTP_304_NOT_MODIFIED, HTTP_404_NOT_FOUND
from src.utilities.custom_logging import cust_logger as logger
from .job_parser_services import SimpJobParserServices
import time


class SimpResToJobScoreServices(ScorerInterface):
    """
    Job-Resume score services
    """

    def __init__(self):
        self.score_parsed_resp = None
        self.parser = common_url_settings.get("SIMPAI_SERVICE")  # 'simplifyai'

    def normalize_resume(self, res_id, client_id):
        result = {}
        try:
            res_schema = PrsResInfSchema()
            res_obj = res_schema.get_by_parser(res_id, client_id, self.parser)
            if res_obj.norm_resp:
                logger.error("Resume Already Normalized")
                result = {"code": HTTP_200_OK,
                          "message": 'Resume Already Normalized',
                          "data": res_obj.norm_resp}
                return result
            '''Call Resume Normalization API '''
            payload = {'idx_id': res_obj.idx_id,
                       'res_id': res_obj.res_id,
                       'clt_id': res_obj.clt_id,
                       'parse_response': json.loads(res_obj.resp)
                       }
            # logger.info("Payload for resume normalization {}".format(json.dumps(payload)))

            simpai_headers = {"accept": "application/json",
                              "content-type": "application/json",
                              # "Authorization": "Bearer " + simpai_url_settings.get("SIMPAI_RESUME_NORM_AUTH_TOKEN", ''),
                              }
            simpai_resume_norm_url = simpai_url_settings.get("SIMPAI_RESUME_NORM_URL")
            logger.info('Resume norm url: {}'.format(simpai_resume_norm_url))
            response = requests.request("POST", headers=simpai_headers,
                                        data=json.dumps(payload),
                                        url=simpai_resume_norm_url)
            logger.info("Response Status for resume normalization %s" % response.status_code)

            if response.status_code == HTTP_200_OK:
                response_info = response.json()
                # logger.info("Response for resume norm: {}".format(json.dumps(response_info)))
                db_resp = res_schema.update_norm_resp(
                    res_obj.res_id, res_obj.clt_id, self.parser,
                    json.dumps(response_info.get('data')))
                if db_resp:
                    logger.info('Norm Resume saved in DB')
                else:
                    logger.error('Norm Resume not saved in DB')
                result = {"code": HTTP_200_OK,
                          "message": "Successfully normalized resume",
                          "data": json.dumps(response_info.get('data'))}
                logger.info("Successfully normalized resume")
            else:
                result = {"code": response.status_code,
                          "message": response.reason,
                          "error": "Resume Norm failed"}
                logger.error("Resume Norm failed")
            return result

        except Exception as ex:
            logger.error("Error in normalizing resume %s " % str(ex))
            result.update({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error in normalizing resume",
                "error": "Error in normalizing resume " + str(ex)
            })
            return result

    def normalize_job(self, job_id, client_id):
        result = {}
        try:
            job_schema = PrsJobInfSchema()
            job_obj = job_schema.get_by_parser(job_id, client_id, self.parser)
            if job_obj.norm_resp:
                logger.error("Job Already Normalized")
                result = {"code": HTTP_200_OK,
                          "message": 'Job Already Normalized',
                          "data": job_obj.norm_resp}
                return result
            '''Call Job Normalization API '''
            payload = {'job': {'index_id': job_obj.index_id,
                               'job_id': job_obj.job_id,
                               'clt_id': job_obj.clt_id,
                               'job_res': job_obj.job_res
                               }
                       }
            # logger.info("Payload for job normalization {}".format(json.dumps(payload)))

            simpai_headers = {"accept": "application/json",
                              "content-type": "application/json",
                              "Authorization": "Bearer " + simpai_url_settings.get("SIMPAI_JOB_NORM_AUTH_TOKEN", ''),
                              }
            simpai_resume_job_url = simpai_url_settings.get("SIMPAI_JOB_NORM_URL")
            logger.info('Resume norm url: {}'.format(simpai_resume_job_url))
            response = requests.request("POST", headers=simpai_headers,
                                        data=json.dumps(payload),
                                        url=simpai_resume_job_url)
            logger.info("Response Status for job normalization %s" % response.status_code)

            if response.status_code == HTTP_200_OK:
                response_info = response.json()
                # logger.info("Response for job norm: {}".format(json.dumps(response_info)))
                db_resp = job_schema.update_norm_resp(
                    job_obj.job_id, job_obj.clt_id, self.parser,
                    json.dumps(response_info.get('data')))
                if db_resp:
                    logger.info('Norm Job saved in DB')
                else:
                    logger.error('Norm Job not saved in DB')
                result = {"code": HTTP_200_OK,
                          "message": "Successfully normalized job",
                          "data": json.dumps(response_info.get('data'))}
                logger.info("Successfully normalized job")
            else:
                result = {"code": response.status_code,
                          "message": response.reason,
                          "error": "Job Norm failed"}
                logger.error("Job Norm failed")
            return result

        except Exception as ex:
            logger.error("Error in normalizing job %s " % str(ex))
            result.update({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error in normalizing job",
                "error": "Error in normalizing job " + str(ex)
            })
            return result

    # def simpai_parse_job_by_id(self, job_id, parse_service='simplifyai'):
    #     payload = {
    #             "job_id": job_id,
    #             "parse_service": parse_service,
    #           }
    #     simpai_headers = {"accept": "application/json",
    #                "content-type": "application/json",
    #                "Authorization": "Bearer " + simpai_url_settings.get("SIMPAI_JOB_PARSER_AUTH_TOKEN", ''),
    #                }

    #     simpai_job_parser_url = simpai_url_settings.get("SIMPAI_JOB_PARSER_URL")
    #     logger.info("Job Parser URL: {}".format(simpai_job_parser_url))
    #     #logger.info("Job Parser Payload : %s " % json.dumps(payload))
    #     result = self.connect_to_api( simpai_headers, payload,
    #                                  simpai_job_parser_url)
    #     return result

    def get_score(self, client_id, resume_id: str, job_id: str, job_category: str) -> dict:
        """
        Parse job with Sovren
        :param resume_id: String
        :param job_id: String
        :return:
        """
        # Check whether JobID and ResumeID exist or not in DB
        score_schema = MatchJResScSchema()
        res_schema = PrsResInfSchema()
        job_schema = PrsJobInfSchema()
        request = None
        result = {}
        logger.info("Client ID in get score: %s " % client_id)

        chk_job_id = job_schema.check_job_id(request, job_id, client_id, self.parser)
        if not chk_job_id:
            result.update({
                "code": HTTP_404_NOT_FOUND,
                "message": "JOB ID not found for this client",
                "error": "JOB ID not found for this client"})
            return result

        chk_res_id = res_schema.check_resume_id(request, resume_id, client_id, self.parser)
        if not chk_res_id:
            result.update({
                "code": HTTP_404_NOT_FOUND,
                "message": "Resume ID not found for this client",
                "error": "Resume ID not found for this client"})
            return result

        get_score = score_schema.get_by_parser(resume_id, job_id, client_id, self.parser)
        formatted_result = {}
        if not get_score:
            logger.info("Score Not Exists in database ")
            '''Check if job and resume are normalized'''
            simp_parser_obj = SimpJobParserServices()
            norm_job = simp_parser_obj.parse_job(client_id, {}, job_id, True)
            # norm_job = self.normalize_job(job_id, client_id)
            if norm_job.get("code") != HTTP_200_OK:
                return norm_job

            norm_res = self.normalize_resume(resume_id, client_id)
            if norm_res.get("code") != HTTP_200_OK:
                return norm_res

            job_index_id = get_job_index(job_id)
            resume_index_id = get_resume_index(resume_id)

            # print("Norm Job:", type(norm_job['data']), norm_job['data'][0:200])
            # print("Norm Resume:", type(norm_res['data']), norm_res['data'][0:100])
            # payload = {
            #         "matchingType": "jobVsResume",
            #         "job_index": job_index_id,
            #         "resume_index": resume_index_id,
            #         "job": json.loads(norm_job['data']),
            #         "resume": json.loads(norm_res['data']),
            #         "job2": {},
            #         "resume2": {}
            #         }
            temp = json.dumps(norm_job['data']['success']['data']['data'])

            payload = {
                "normalized_job": json.loads(temp),
                "normalized_resume": json.loads(norm_res['data']),
                "weights": {
                    "title_weight": 0.05,
                    "experience_weight": 0.2,
                    "education_weight": 0.05,
                    "certification_weight": 0.1,
                    "skill_weight": 0.4,
                    "job_type_weight": 0.125,
                    "location_weight": 0.025,
                    "industry_weight": 0.05
                }
            }
            payload = json.dumps(payload)

            simpai_headers = {"accept": "application/json",
                              "content-type": "application/json",
                              "Authorization": "Bearer " + simpai_url_settings.get("SIMPAI_MATCHER_AUTH_TOKEN", ''),
                              }
            request_url = simpai_url_settings.get("SIMPAI_MATCHER_URL")

            result = self.connect_to_api(simpai_headers, payload, request_url)

            if result.get("code") != HTTP_200_OK:
                return result

            # Save response to DB
            data = {}
            data.update({
                "job_id": job_id,
                "job_idx_id": job_index_id,
                "res_id": resume_id,
                "res_idx_id": resume_index_id,
                "scr_res": result.get('data'),
                "clt_id": client_id
            })

            if result.get("code") == HTTP_200_OK:
                data_to_save = score_schema.add(request, data, self.parser)

                if data_to_save:
                    logger.info("Parsed Score Saved in DB ")
                    result.update({
                        "saved_in_DB": True
                    })
                else:
                    logger.info("Parsed Score NOT Saved in DB ")
                    result.update({
                        "saved_in_DB": False
                    })

                display_data = json.loads(result.get('data'))
                # display_data = display_data.get('Value', {}).get('Matches', [])
                # display_data = json.loads(json.dumps(display_data))

                formatted_result.update({
                    "code": result.get('code'),
                    "message": result.get('message'),
                    "data": display_data
                })
                self.score_parsed_resp = result.get('data')
                return formatted_result

        else:
            logger.info("Score Already Exists in database ")
            score_resp = get_score.scr_res

            display_data = json.loads(get_score.scr_res)
            # display_data = display_data.get('Value', {}).get('Matches', [])
            # display_data = json.loads(json.dumps(display_data))

            formatted_result.update({
                "code": HTTP_304_NOT_MODIFIED,
                "message": "Duplicate Score",
                "data": display_data
            })
            self.score_parsed_resp = get_score.scr_res
            return formatted_result

        pass

    def connect_to_api(self, header: dict, payload: dict,
                       calling_api: str) -> dict:
        """
        Match's resume with it's index id to a job with job index id and job
        document id and get's score from sovren
        :param index_to_search: String
        :param job_index_id: String
        :param job_document_id: String
        :param resume_document_id: String
        :return: String
        """
        result = {}
        try:
            # time.sleep(2)
            # logger.info("Payload for Simpai Score {}".format(json.dumps(payload)))
            start = time.time()
            response = requests.request("POST", headers=header, data=payload, url=calling_api)
            
            
            logger.info("Response Status for Simpai Score %s" % response.status_code)

            if response.status_code == 200:

                response_info = response.json()
                logger.info("Response for Simpai Score {}".format(response_info))
                result = {"code": HTTP_200_OK,
                          "message": "Successfully generated score from Simpai",
                          "data": json.dumps(response_info)}
                logger.info("Successfully generated score from Simpai")
            else:
                result = {"code": response.status_code,
                          "message": response.reason,
                          "error": "Simpai unable to proces the request"}
                logger.error("Simpai unable to proces the request ")
            result = result
            end = time.time()
            logger.info("Simplifyai Matcher time taken to process Score %s" % (end -start))
            return result

        except Exception as ex:
            logger.error("Error in generating score from Simpai %s " % str(ex))
            result.update({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error while generating score from Simpai",
                "error": "Error in generating score from Simpai " + str(ex)
            })
            return result

