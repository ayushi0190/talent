# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Get Resume to Job Score from sovren services
@author <AnkitS@simplifyvms.com>
"""
import time
import json
from abc import ABC
from fastapi import Request
import requests
from requests.exceptions import RequestException
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR,\
                             HTTP_304_NOT_MODIFIED, HTTP_404_NOT_FOUND
import time

from src.services.common.config.common_config import common_url_settings
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.sovren.helpers.misc_helpers import (get_sovren_headers)
from src.services.sovren.interfaces.scorers.scorer_interface import ScorerInterface
from src.db.crud.sovren.match_j_res_sc_schema import MatchJResScSchema
from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from src.db.crud.sovren.prs_jobs_inf_schema import PrsJobInfSchema
from src.services.sovren.helpers.misc_helpers import (get_job_index,
                                                      get_resume_index)
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema
from src.db.crud.admin.clt_cat_wgt_schema import CltCatWgtSchema


class ResToJobScoreServices(ScorerInterface, ABC):
    """
    Job board services
    """

    def __init__(self):
        self.score_parsed_resp = None
        self.parser = common_url_settings.get("SOVREN_SERVICE") #'sovren'

    def distribute_cat_weights(self, client_id: str,
                               job_resp: dict, cat_weights: dict):
        '''
        Sample output for Sovren parsed job
        {
          "education": [],
          "languages": [],
          "exec_type": [],
          "mgmt_level": [],
          "job_titles": [],
          "certifications": [],
          "skills": [],
        }
        Sample cat weight for client
        {
          "job_category": "default",
          "category_weights": {
            "EDUCATION": 0.15,
            "JOB_TITLES": 0.15,
            "SKILLS": 0.25,
            "INDUSTRIES": 0.10,
            "LANGUAGES": 0,
            "CERTIFICATIONS": 0.15,
            "EXECUTIVE_TYPE": 0,
            "MANAGEMENT_LEVEL": 0.20
          }
        }
        Sample category_weight for sovren scoring
        cat_weights =
        [{ "Category": "SKILLS",
            "Weight": 0.75
         },
         { "Category": "",
            "Weight": 0.25
        }]
        '''
        result = []

        # Find avalibale job sections with valid data
        all_job_cat = ['EDUCATION','JOB_TITLES','SKILLS','INDUSTRIES','LANGUAGES',
                   'CERTIFICATIONS','EXECUTIVE_TYPE','MANAGEMENT_LEVEL']
        job_sec = self.find_parsed_job_sections(job_resp)
        print('Job sections: {}'.format(job_sec))
        #nz_job_cat = set(all_job_cat)
        nz_job_cat = set()
        for key, val in job_sec.items():
            if val:
                nz_job_cat.add(key)
        # Find non-zero weight categories
        nz_cat = set()
        for key, val in cat_weights.items():
            if val > 0:
                nz_cat.add(key)
        # Find common non-zero weight
        comm_cat = nz_job_cat & nz_cat
        if len(comm_cat) == 0:
            print("Unexpected condition: Non-zero cat are not present in job")
            result = []
        elif len(cat_weights) == len(comm_cat):
            print("All non-zero cat are present in job")
            result = []
        elif len(comm_cat) == 1:
            result = [{"Category": list(comm_cat)[0], "Weight": 1}]
        else:
            zero_cat_sum = sum([cat_weights[cat] for cat in cat_weights if cat not in comm_cat])
            zero_cat_cnt = len(comm_cat)
            print('Missing cat total weight: {} and Non-zero cat count: {}'
                  .format(zero_cat_sum, zero_cat_cnt))
            for cat in comm_cat:
                result.append({
                        "Category": cat,
                        "Weight": round(cat_weights[cat] + (zero_cat_sum / zero_cat_cnt), 4)
                        })
        return result

    def get_score(self, request, resume_id: str, job_id: str,
                  job_category: str, category_weights: dict) -> dict:
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
        audit_model = AuditTrailsSchema()
        service_name = request.url.path
        wgt_obj = CltCatWgtSchema()

        # Get Client ID from HEADERS
        client_id = request.headers["client_id"]
        result = {}

        request.app.logger.info("Client ID in get score: %s " % client_id)
        '''
        chk_job_id = job_schema.check_job_id(request, job_id, client_id)
        if not chk_job_id:
            result.update({
                "code": HTTP_404_NOT_FOUND,
                "message": "JOB ID not found for this client",
                "error": "JOB ID not found for this client"})
            return result
        '''

        job_resp = job_schema.get_by_parser(job_id, client_id, self.parser)
        if not job_resp:
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

        get_score = score_schema.get_by_parser(resume_id,job_id, client_id, self.parser)
        formatted_result = {}
        if not get_score:

            job_index_id = get_job_index(job_id)
            resume_index_id = get_resume_index(resume_id)

            request.app.logger.info("Not Exists in database ")
            '''
            payload = {
                "IndexIdsToSearchInto": [
                    resume_index_id
                ],
                "Take": 0,
                "CategoryWeights": [
                    {
                        "Category": sovren_url_settings.get("CATEGORY1"),
                        "Weight": sovren_url_settings.get("WEIGHT1")
                    },
                    {
                        "Category": sovren_url_settings.get("CATEGORY2"),
                        "Weight": sovren_url_settings.get("WEIGHT2")
                    }

                ],
                "FilterCriteria": {
                    "DocumentIds": [
                        resume_id
                    ],
                    "CustomValueIds": [
                        ""
                    ]
                }
            }
            '''
            payload = {
                "IndexIdsToSearchInto": [
                    resume_index_id
                ],
                "Take": 0,
                "FilterCriteria": {
                    "DocumentIds": [
                        resume_id
                    ],
                    "CustomValueIds": [
                        ""
                    ]
                }
            }

            # Find job_category from job details or parsed job
            parsed_job = json.loads(job_resp.job_res).get('Value', '{}')
            parsed_job = json.loads(parsed_job.get('ParsedDocument', '{}'))
            new_weights = []
            if category_weights:
                request.app.logger.info("Category weights in request"
                                        .format(category_weights))
                new_weights = self.distribute_cat_weights(
                            client_id, parsed_job, category_weights)
            else:
                cat_weights = wgt_obj.get_cat_weights(client_id, job_category)
                if not cat_weights:
                    def_job_cat = common_url_settings.get('DEFAULT_JOB_CATEGORY')
                    def_weights = wgt_obj.get_cat_weights(client_id, def_job_cat)
                    if def_weights:
                        request.app.logger.info("Default category weights: {}"
                                                .format(def_weights.cat_weights))
                        new_weights = self.distribute_cat_weights(
                                client_id, parsed_job, def_weights.cat_weights)
                    else:
                        request.app.logger.info("Default cat weight not found")
                        new_weights = []
                else:
                    request.app.logger.info("Category weight in DB: {}"
                                            .format(cat_weights.cat_weights))
                    new_weights = self.distribute_cat_weights(
                            client_id, parsed_job, cat_weights.cat_weights)

            if new_weights:
                payload['CategoryWeights'] = new_weights
                pass
            request.app.logger.info("Using new weight after distribution: {}"
                                    .format(new_weights))

            request_url = sovren_url_settings.get("SOVREN_MATCH_DOCUMENT_BY_ID_URL") + \
                           job_index_id + '/documents/' + job_id

            result = self.connect_to_api(request, get_sovren_headers(), payload, request_url)

            if result.get("code") != HTTP_200_OK:
                return result

            #Save response to DB
            data = {}
            data.update({
                "job_id" : job_id,
                "job_idx_id": job_index_id,
                "res_id": resume_id,
                "res_idx_id": resume_index_id,
                "scr_res": result.get('data'),
                "clt_id": client_id
            })

            if result.get("code") == HTTP_200_OK:
                data_to_save = score_schema.add(request,data, self.parser)

                if data_to_save:
                    request.app.logger.info("Parsed Score Saved in DB ")
                    result.update({
                        "saved_in_DB": True
                    })
                else:
                    request.app.logger.info("Parsed Score NOT Saved in DB ")
                    result.update({
                        "saved_in_DB": False
                    })

                display_data = json.loads(result.get('data'))
                display_data = display_data.get('Value', {}).get('Matches', [])
                display_data = json.loads(json.dumps(display_data))

                formatted_result.update({
                    "code": result.get('code'),
                    "message": result.get('message'),
                    "data": display_data
                })
                self.score_parsed_resp = result.get('data')
                if service_name != "/submission":
                    audit_model.add(service_name,client_id)
                return formatted_result

        else:
            request.app.logger.info("Score Already Exists in database ")
            score_rsep = get_score.scr_res

            display_data = json.loads(get_score.scr_res)
            display_data = display_data.get('Value', {}).get('Matches', [])
            display_data = json.loads(json.dumps(display_data))

            formatted_result.update({
                "code": HTTP_304_NOT_MODIFIED,
                "message": "Duplicate Score",
                "data": display_data
            })
            self.score_parsed_resp = get_score.scr_res
            if service_name != "/submission":
                audit_model.add(service_name,client_id)
            return formatted_result

    def connect_to_api(self, request, header: dict, payload: dict,
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
            time.sleep(2)
            request.app.logger.info("Payload for Sovren Score {}".format(json.dumps(payload)))
            start = time.time()
            response = requests.request("POST", headers=header, data=json.dumps(payload), url=calling_api)
            request.app.logger.info("Response Status for Sovren Score %s" % response.status_code)

            response_info = response.json()
            request.app.logger.info("Response for Sovren Score %s" % json.dumps(response_info))
            if response.status_code == 200:

                request.app.logger.info("Response for Sovren Score {}".format(response_info))
                result = {"code": HTTP_200_OK,
                          "message": "Successfully generated score from Sovren",
                          "data": json.dumps(response_info)}
                request.app.logger.info("Successfully generated score from Sovren")
            else:
                msg = response_info.get('Info', {}).get('Message','')
                result ={"code": response.status_code,
                         "message": msg,
                         "error": "Sovren unable to proces the request"}
                request.app.logger.info("Sovren unable to proces the request: " + str(msg))
            result = result
            end = time.time()
            request.app.logger.info("Time taken for sovren to generate Score %s" % (end - start))
            return result

        except Exception as ex:
            request.app.logger.info("Error in generating score from Sovren %s " % str(ex))
            result.update({
                "code":  HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error while generating score from Sovren",
                "error": "Error in generating score from Sovren " + str(ex)
            })
            return result

    def find_parsed_job_sections(self, parsed_job: dict):
        result = {}
        all_job_cat = ['EDUCATION','JOB_TITLES','SKILLS','INDUSTRIES','LANGUAGES',
                   'CERTIFICATIONS','EXECUTIVE_TYPE','MANAGEMENT_LEVEL']
        start_point = parsed_job.get('SovrenData',{})
        #start_point = parsed_job.get('ParsedDocument',{}).get('SovrenData',{})
        if not start_point:
            print('Keys missing in parsed job: {}'.format(start_point.keys()))
            return result

        '''Currently industry category is assumed to be present in job  '''
        result['INDUSTRIES'] = True
        result['MANAGEMENT_LEVEL'] = True
        management_level = start_point.get("ManagementLevel", None)
        if management_level:
            if management_level.lower() == "none":
                result['MANAGEMENT_LEVEL'] = False
        else:
            result['MANAGEMENT_LEVEL'] = False

        result['EXECUTIVE_TYPE'] = True
        exec_type = start_point.get("ExecutiveType", None)
        if exec_type:
            if exec_type.lower() == "none":
                result['EXECUTIVE_TYPE'] = False
        else:
            result['EXECUTIVE_TYPE'] = False

        result['JOB_TITLES'] = True
        main_job_title = start_point.get("JobTitles", {}).get('MainJobTitle','')
        job_titles = start_point.get("JobTitles", {}).get('JobTitle',[])
        if job_titles or main_job_title:
            if (len(job_titles) == 0 or job_titles[0].strip() == '') \
            and main_job_title.strip() == '':
                result['JOB_TITLES'] = False
        else:
            result['JOB_TITLES'] = False

        result['CERTIFICATIONS'] = True
        certifications = start_point.get("CertificationsAndLicenses", {}) \
                                    .get('CertificationOrLicense', [])
        if certifications:
            if len(certifications) == 0 or certifications[0].strip() == '':
                result['CERTIFICATIONS'] = False
        else:
            result['CERTIFICATIONS'] = False

        result['EDUCATION'] = True
        education = start_point.get("Education", {}).get('Degree',[])
        if education:
            if len(education) == 0 or education[0].get('DegreeType', '') == '':
                result['EDUCATION'] = False
        else:
            result['EDUCATION'] = False

        result['LANGUAGES'] = True
        languages = start_point.get("LanguageCodes", {}).get('LanguageCode', [])
        if languages:
            if len(languages) == 0 or languages[0].strip() == '':
                result['LANGUAGES'] = False
        else:
            result['LANGUAGES'] = False

        result['SKILLS'] = True
        skills_taxonomy = start_point.get("SkillsTaxonomyOutput", [])
        if not skills_taxonomy:
            result['SKILLS'] = False
        else:
            taxonomy = skills_taxonomy[0].get('Taxonomy', [])
            if not taxonomy:
                result['SKILLS'] = False
            else:
                sub_taxonomy = taxonomy[0].get('Subtaxonomy', [])
                if not sub_taxonomy:
                    result['SKILLS'] = False
                else:
                    skills = sub_taxonomy[0].get('Skill', [])
                    if skills:
                        if len(skills) == 0 or skills[0].get('@name').strip() == '':
                            result['SKILLS'] = False
                    else:
                        result['SKILLS'] = False

        return result
