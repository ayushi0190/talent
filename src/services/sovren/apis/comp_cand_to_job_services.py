# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Compare Candidate
@author <AnkitS@simplifyvms.com>
"""

import json
import re
from abc import ABC
from datetime import datetime, timedelta, timezone

import requests
from iteration_utilities import unique_everseen
from starlette.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND)

from src.db.crud.sovren.candidates_to_job_schema import CandidatesToJobSchema
from src.db.crud.sovren.mp_tp_res_schema import MpTpResSchema
from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from src.db.crud.sovren.match_j_res_sc_schema import MatchJResScSchema
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.sovren.helpers.misc_helpers import (
    get_addr_from_postal_addr, get_all_skills, get_candidate_location,
    get_certification, get_detail_parsed_information, get_distance,
    get_job_details, get_languages, get_parsed_education,
    get_parsed_experience, get_parsed_skills1,
    search_resume_in_internal_buckets, get_resume_index)
from src.services.sovren.interfaces.comp_cand_interface import (
    CompareCandidateInput, CompareCandidateInterface)
from src.db.crud.sovren.intern_res_schema import InternResSchema
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema
from src.services.common.config.common_config import common_url_settings

class CompCandToJobServices(CompareCandidateInterface, ABC):
    """
    Compare Candidate services class

    """

    @staticmethod
    def list_compare_candidates_info_with_sovren(request,
            payload: CompareCandidateInput):
        """
        List candidates info with sovren
        :param data:
        :return:
        """
        result = {}
        final_result = []
        extracted_data = {}
        audit_model = AuditTrailsSchema()
        service_name = request.url.path
        clt_id = request.headers['client_id']
        parser = common_url_settings.get("SOVREN_SERVICE") #'sovren'

        candidates_list = CandidatesToJobSchema. \
            get_candidates_search_result(payload.JobId)
        request.app.logger.info("Discover Candidates already performed %s " % candidates_list)
        job_details = get_job_details(payload.JobId)

        if job_details["status-code"] != HTTP_200_OK:
            extracted_data.update(
                {
                    "code": HTTP_400_BAD_REQUEST,
                    "message": "Unable to perform operation," +
                    "job reference id does not match with the given",
                })
            return extracted_data

        job_location = job_details.get("result")[0].get("job"). \
            get("job_location").strip()
        job_company = ''
        if job_details.get("result")[0].get("job"). \
                get("company_name"):
            job_company = job_details.get("result")[0].get("job"). \
                get("company_name").strip()
        try:
            for cnt, resume in enumerate(payload.resume_id):
                if candidates_list:
                    check_res_list = [res_id.get("Id") for res_id in candidates_list.srch_res]
                    if resume in check_res_list:
                        request.app.logger.info("Resume Id matching in Disover Candidates %s " % resume)
                        for matched_resume in candidates_list.srch_res:
                            if resume == matched_resume.get("Id"):
                                resume_info, all_skills, exp_data, educ_data, cert_name, \
                                    language_details, candidate_location = CompCandToJobServices.\
                                    get_resumes_info(resume, job_location)
                                request.app.logger.info("Resume Info retrived %s " % resume_info)
                                if matched_resume.get("UnWeightedScore")[0]. \
                                        get("Category") == "SKILLS":
                                    compared_value = CompCandToJobServices.get_compared_value(
                                        matched_resume.get("UnWeightedScore")[0]. get("TermsFound"), resume_info)

                                    additional_skill_values = CompCandToJobServices.get_additional_skills_values(
                                        matched_resume.get("UnWeightedScore")[0].
                                        get("TermsFound"), resume_info
                                    )
                                
                                    matched_skills = CompCandToJobServices.get_matched_skills(
                                        compared_value)
                                    request.app.logger.info("Matched Skills retrived %s " % matched_skills)

                                    get_additional_skills = CompCandToJobServices.get_additional_skills(
                                        matched_skills, additional_skill_values)

                                    get_most_used_skills = CompCandToJobServices.most_used_skills(
                                        get_additional_skills)
                                    request.app.logger.info("Most Used Skills retrived %s " % get_most_used_skills)

                                    latest_used_skills = CompCandToJobServices.latest_used_skills(
                                        matched_skills, get_additional_skills)
                                    request.app.logger.info("Latest Used Skills retrived %s " % latest_used_skills)

                                    result.update({
                                        resume: {}
                                    })

                                    matched_resume = matched_resume.get("UnWeightedScore")
                                    weighted_score = matched_resume.get("WeightedScore",0)
                                    request.app.logger.info("Weighted Score if it is from can_to_job_model %s "
                                                            % weighted_score)
                                    industries = CompCandToJobServices.get_industries(
                                        matched_resume)

                                    worked_in_same_org = False
                                    if exp_data and len(exp_data) > 0:
                                        if job_company and exp_data[0].get("Organization Name"):
                                            comp_list = [cmp_data.get('Organization Name') for cmp_data in exp_data]
                                            if job_company in comp_list:
                                                worked_in_same_org = True
                                    result[resume].update({
                                        "WeightedScore": weighted_score,
                                        "MatchedSkills": matched_skills,
                                        "TopSkills": {
                                            "MostUsed": get_most_used_skills,
                                            "LatestUsed": latest_used_skills
                                        },
                                        "AllSkills": all_skills,
                                        "Experience": exp_data,
                                        "EducationDetail": educ_data,
                                        "Certification": cert_name,
                                        "LanguageKnown": language_details,
                                        "CandidateLocation": candidate_location,
                                        "Industries": industries,
                                        "WorkedInSameOrg": worked_in_same_org
                                    })
                    else:
                        request.app.logger.info("Resume Id not matching in Disover Candidates %s " % resume)
                        scored_resume = MatchJResScSchema().get_scored_resume(
                                resume,payload.JobId, clt_id, parser)
                        if scored_resume:
                            resume_info, all_skills, exp_data, educ_data, cert_name, \
                                language_details, candidate_location = CompCandToJobServices.\
                                get_resumes_info(resume, job_location)
                            request.app.logger.info("Resume Info retrived %s " % resume_info)
                            ext_resume = json.loads(scored_resume.scr_res)
                            matched_resume = ext_resume['Value']['Matches'][0]['UnweightedCategoryScores']
                            if matched_resume[0]. \
                                    get("Category") == "SKILLS":
                                compared_value = CompCandToJobServices.get_compared_value(
                                    matched_resume[0].get("TermsFound"), resume_info)

                                additional_skill_values = CompCandToJobServices.get_additional_skills_values(
                                    matched_resume[0].
                                    get("TermsFound"), resume_info
                                )

                                matched_skills = CompCandToJobServices.get_matched_skills(
                                    compared_value)
                                request.app.logger.info("Matched Skills retrived %s " % matched_skills)

                                get_additional_skills = CompCandToJobServices.get_additional_skills(
                                    matched_skills, additional_skill_values)

                                get_most_used_skills = CompCandToJobServices.most_used_skills(
                                    get_additional_skills)
                                request.app.logger.info("Most Used Skills retrived %s " % get_most_used_skills)

                                latest_used_skills = CompCandToJobServices.latest_used_skills(
                                    matched_skills, get_additional_skills)
                                request.app.logger.info("Latest Used Skills retrived %s " % latest_used_skills)

                                result.update({
                                    resume: {}
                                })

                                industries = CompCandToJobServices.get_industries(
                                    matched_resume)
                                weighted_score = ext_resume.get('Value',{})
                                weighted_score = weighted_score.get('Matches', [])
                                request.app.logger.info("Length of Weighted Score if it is from mat_j_res_scr_model"
                                                        " %s " % str(len(weighted_score)))
                                if len(weighted_score) == 0:
                                    weighted_score = 0
                                else:
                                    weighted_score = weighted_score[0]
                                    weighted_score = weighted_score.get('WeightedScore',0)
                                    request.app.logger.info("Weighted Score if it is from "
                                                            "mat_j_res_scr_model %s " % weighted_score)
                                worked_in_same_org = False
                                if exp_data and len(exp_data) > 0:
                                    if job_company and exp_data[0].get("Organization Name"):
                                        comp_list = [cmp_data.get('Organization Name') for cmp_data in exp_data]
                                        if job_company in comp_list:
                                            worked_in_same_org = True
                                result[resume].update({
                                    "WeightedScore": weighted_score,
                                    "MatchedSkills": matched_skills,
                                    "TopSkills": {
                                        "MostUsed": get_most_used_skills,
                                        "LatestUsed": latest_used_skills
                                    },
                                    "AllSkills": all_skills,
                                    "Experience": exp_data,
                                    "EducationDetail": educ_data,
                                    "Certification": cert_name,
                                    "LanguageKnown": language_details,
                                    "CandidateLocation": candidate_location,
                                    "Industries": industries,
                                    "WorkedInSameOrg": worked_in_same_org
                                })
                        else:
                            request.app.logger.info(" Resume ID: %s has no submission against this job " % resume)
                            result = {
                                "code" : HTTP_404_NOT_FOUND,
                                "message" : "Resume ID: {} has no submission against this job".format(resume)
                            }
                            break
                else:
                    request.app.logger.info("Start Disover Candidates %s " % resume)
                    scored_resume = MatchJResScSchema().get_scored_resume(
                            resume,payload.JobId, clt_id, parser)
                    if scored_resume:
                        resume_info, all_skills, exp_data, educ_data, cert_name, \
                            language_details, candidate_location = CompCandToJobServices.\
                            get_resumes_info(resume, job_location)
                        request.app.logger.info("Resume Info retrived %s " % type(resume_info))
                        ext_resume = json.loads(scored_resume.scr_res)
                        weighted_score = ext_resume.get('Value', {})
                        weighted_score = weighted_score.get('Matches', [])
                        request.app.logger.info("Length of Weighted Score if discovery has not "
                                                "performed %s " % str(len(weighted_score)))
                        if len(weighted_score) == 0:
                            weighted_score = 0
                        else:
                            weighted_score = weighted_score[0]
                            weighted_score = weighted_score.get('WeightedScore', 0)
                            request.app.logger.info("Weighted Score if if discovery has not performed"
                                                    "and it is from mat_j_res_scr_model %s " % weighted_score)

                        matched_resume = ext_resume['Value']['Matches'][0]['UnweightedCategoryScores']
                        if matched_resume[0]. \
                                get("Category") == "SKILLS":
                            compared_value = CompCandToJobServices.get_compared_value(
                                matched_resume[0].get("TermsFound"), resume_info)

                            additional_skill_values = CompCandToJobServices.get_additional_skills_values(
                                matched_resume[0].
                                get("TermsFound"), resume_info
                            )

                            matched_skills = CompCandToJobServices.get_matched_skills(
                                compared_value)
                            request.app.logger.info("Matched Skills retrived %s " % matched_skills)

                            get_additional_skills = CompCandToJobServices.get_additional_skills(
                                matched_skills, additional_skill_values)

                            get_most_used_skills = CompCandToJobServices.most_used_skills(
                                get_additional_skills)
                            request.app.logger.info("Most Used Skills retrived %s " % get_most_used_skills)

                            latest_used_skills = CompCandToJobServices.latest_used_skills(
                                matched_skills, get_additional_skills)
                            request.app.logger.info("Latest Used Skills retrived %s " % latest_used_skills)

                            result.update({
                                resume: {}
                            })

                            industries = CompCandToJobServices.get_industries(
                                matched_resume)

                            worked_in_same_org = False
                            if exp_data and len(exp_data) > 0:
                                if job_company and exp_data[0].get("Organization Name"):
                                    comp_list = [cmp_data.get('Organization Name') for cmp_data in exp_data]
                                    if job_company in comp_list:
                                        worked_in_same_org = True
                            result[resume].update({
                                "WeightedScore": weighted_score,
                                "MatchedSkills": matched_skills,
                                "TopSkills": {
                                    "MostUsed": get_most_used_skills,
                                    "LatestUsed": latest_used_skills
                                },
                                "AllSkills": all_skills,
                                "Experience": exp_data,
                                "EducationDetail": educ_data,
                                "Certification": cert_name,
                                "LanguageKnown": language_details,
                                "CandidateLocation": candidate_location,
                                "Industries": industries,
                                "WorkedInSameOrg": worked_in_same_org
                            })
                    else:
                        request.app.logger.info(" Resume ID: %s has no submission against this job " % resume)
                        result = {
                            "code" : HTTP_404_NOT_FOUND,
                            "message" : "Resume ID: {} has no submission against this job".format(resume)
                        }
                        break
            if result.get('code') != HTTP_404_NOT_FOUND:
                audit_model.add(service_name,clt_id)
            final_result = [result]
            return final_result
        except Exception as ex:
            result = {}
            request.app.logger.info("Error in Performing Compare Candidates %s " % str(ex))
            result.update({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error in perfrming compare candidates ",
                "error": "Exception is :" + str(ex)
            })
            return result

    @staticmethod
    def get_missing_candidate_location(data, job_location):
        """
        Get missing candidate location
        :param data:
        :param job_location:
        :return:
        """
        candidate_location = []
        if data and job_location:
            for index, element in enumerate(data):
                if "PostalAddress" in element:
                    postal_address = element["PostalAddress"]
                    addr = get_addr_from_postal_addr(element)
                    distance_to_work = get_distance(job_location, addr)
                    candidate_location.append({
                        "Country Code": postal_address.get("CountryCode", ""),
                        "Postal Code": postal_address.get("PostalCode", ""),
                        "Region": postal_address.get("Region")[0] if
                        postal_address.get("Region") else "",
                        "Municipality": postal_address.get("Municipality", ""),
                        "Distance to Work": distance_to_work
                    })
        return candidate_location

    @staticmethod
    def get_candidate_info(resume_id):
        """
        Get candidate information
        :param resume_id:
        :return:
        """
        try:
            contact_info = sovren_url_settings.RESUME_SCORE.contact_info_from_talent_pool
            info = contact_info.find_one(
                {'resume_id': re.compile(resume_id, re.IGNORECASE)})
            return info['ContactInfo']
        except Exception as es_res:
            print("Unable to connect: '%s'", es_res)

    @staticmethod
    def get_industries(data):
        """
        Get industries
        :param data:
        :return:
        """
        if data:
            if isinstance(data, list):
                for index, element in enumerate(data):
                    if isinstance(element, dict):
                        if element.get("Category") == "INDUSTRIES":
                            return element.get("TermsFound")
            else:
                # for index, element in enumerate(data.get("UnWeightedScore")):
                if isinstance(data, dict):
                    if data.get("Category") == "INDUSTRIES":
                        return data.get("TermsFound")

    @staticmethod
    def latest_used_skills(skills_to_match, additional_skills):
        """
        Get latest used skills
        :param skills_to_match:
        :param additional_skills:
        :return:
        """
        result_list = []
        final_output = []
        if skills_to_match and additional_skills:
            for x_val in additional_skills:
                match = 0
                for y_val in skills_to_match:
                    if x_val['Name'] == y_val['Name']:
                        match = 1
                if x_val['TotalMonths'] and x_val['LastUsed'] and match == 0:
                    result_list.append(x_val)
            current_date = datetime.now()
            for x_val in result_list:
                used_date = datetime.strptime(x_val["LastUsed"],
                                              "%Y-%m-%d").date()
                if used_date.year <= current_date.year:
                    final_output.append(x_val)
            final_output = list(unique_everseen(final_output))
            final_output.sort(key=lambda x: (x['LastUsed']), reverse=True)
            if len(final_output) > 3:
                final_output = final_output[:3]
        return final_output

    @staticmethod
    def most_used_skills(additional_skills):
        """
        Get most used skills
        :param additional_skills:
        :return:
        """
        result_list = []
        if additional_skills:
            for x_val in additional_skills:
                if x_val['Name'] and (
                        x_val['TotalMonths'] and x_val['LastUsed']):
                    result_list.append(x_val)
            if len(result_list) > 0:
                result_list.sort(
                    key=lambda x: (
                        x['TotalMonths']),
                    reverse=True)
            if len(result_list) > 3:
                result_list = result_list[:3]
        return result_list

    @staticmethod
    def get_additional_skills(matched_skills, compared_value):
        """
        Get additional skills
        :param matched_skills:
        :param compared_value:
        :return:
        """
        result_list = []
        if matched_skills and compared_value:
            for x_val in compared_value:
                match = 0
                for y_val in matched_skills:
                    if x_val['Name'] == y_val['Name']:
                        match = 1
                if x_val['TotalMonths'] and x_val['LastUsed'] and match == 0:
                    result_list.append(x_val)
            result_list = list(unique_everseen(result_list))
            if len(result_list) > 6:
                result_list = result_list[:6]
        return result_list

    @staticmethod
    def get_matched_skills(compared_value):
        """
        Get matched skills
        :param compared_value:
        :return:
        """
        date_compared_list = []
        if compared_value:
            for index, items in enumerate(compared_value):
                if items["LastUsed"]:
                    used_date = datetime.strptime(items["LastUsed"],
                                                  "%Y-%m-%d").date()
                    date_compared_list.append({
                        "Name":
                            items["Name"],
                        "TotalMonths":
                            items["TotalMonths"],
                        "LastUsed":
                            used_date
                    })
            date_compared_list.sort(
                key=lambda x: (
                    x['LastUsed']),
                reverse=True)
        return date_compared_list

    @staticmethod
    def get_compared_value(skill_set, extracted_results):
        """
        Compare skill set from job to candidate matching with
        candidate resume
        :param skill_set:
        :param extracted_results:
        :return:
        """
        skill_data = []
        if extracted_results:
            for index, tax_element in extracted_results.items():
                if isinstance(tax_element, dict):
                    for sub_tax_idx, sub_tax_ele in \
                            tax_element.items():
                        if isinstance(sub_tax_ele, dict):
                            for skill_idx, skill_ele in \
                                    sub_tax_ele.items():
                                if isinstance(skill_ele, dict):
                                    if any(ele in skill_ele["Name"] for
                                           ele in skill_set):
                                        skill_data.append({
                                            "Name":
                                                skill_ele["Name"],
                                            "TotalMonths":
                                                skill_ele["TotalMonths"],
                                            "LastUsed":
                                                skill_ele["LastUsed"]
                                        })

        return list(unique_everseen(skill_data))

    @staticmethod
    def get_additional_skills_values(skill_set, extracted_results):
        """
        Compare skill set from job to candidate matching with
        candidate resume
        :param skill_set:
        :param extracted_results:
        :return:
        """
        skill_data = []
        if extracted_results:
            for index, tax_element in extracted_results.items():
                if isinstance(tax_element, dict):
                    for sub_tax_idx, sub_tax_ele in \
                            tax_element.items():
                        if isinstance(sub_tax_ele, dict):
                            for skill_idx, skill_ele in \
                                    sub_tax_ele.items():
                                if isinstance(skill_ele, dict):
                                    if skill_ele["Name"] not in skill_set:
                                        skill_data.append({
                                            "Name":
                                                skill_ele["Name"],
                                            "TotalMonths":
                                                skill_ele["TotalMonths"],
                                            "LastUsed":
                                                skill_ele["LastUsed"]
                                        })

        return list(unique_everseen(skill_data))

    @staticmethod
    def get_resumes_info(resume_id, job_location):
        """
        Get resume information
        :param job_location:
        :param resume_id:
        :return:
        """
        filtered_result = None
        educ_data = None
        exp_data = None
        cert_name = None
        language_details = None
        all_skills = None
        candidate_location = None

        resume = PrsResInfSchema().get(resume_id)
        if resume:
            parsed_resume_section = json.loads(json.loads(
                resume.resp)['Value']['ParsedDocument'])
            resume_text = parsed_resume_section
            filtered_result = get_detail_parsed_information(
                resume_text["Resume"])
            parsed_resume = resume_text["Resume"]
            educ_data, exp_data, cert_name, language_details, \
                all_skills, candidate_location = CompCandToJobServices. \
                get_other_parsed_information(parsed_resume, job_location)
        else:
            resume = InternResSchema().get(resume_id)
            parsed_resume_section = json.loads(json.loads(
                resume.resp)['Value']['ParsedDocument'])
            resume_text = parsed_resume_section
            filtered_result = get_detail_parsed_information(
                resume_text["Resume"])
            parsed_resume = resume_text["Resume"]
            educ_data, exp_data, cert_name, language_details, \
                all_skills, candidate_location = CompCandToJobServices. \
                get_other_parsed_information(parsed_resume, job_location)

        return filtered_result, all_skills, exp_data, \
            educ_data, cert_name, \
            language_details, candidate_location

    @staticmethod
    def get_other_parsed_information(data, job_location):
        """
        Other parsed information
        :param job_location:
        :param data:
        :return:
        """
        # final_data = []
        if data:
            data1 = data.get("StructuredXMLResume")

            # skill_data1 = get_parsed_skill(data)
            # final_data.append(skill_data1)

            educ_data = get_parsed_education(data1)
            # final_data.append(educ_data)

            exp_data = get_parsed_experience(data1)

            # work_location = get_work_location(data1)

            cert_name = get_certification(data1)

            language_details = get_languages(data1)

            all_skills = get_all_skills(data)

            candidate_location = get_candidate_location(data1, job_location)

            skill_taxonomy = get_parsed_skills1(data)

        return educ_data, exp_data, cert_name, language_details, \
            all_skills, candidate_location
