# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Searcher related services
@author <rchakraborty@simplifyvms.com>
@author <sreddy@simplifyvms.com>
@author <satya@simplifyvms.com>
"""
from typing import Dict

from fastapi import status
from pydantic import ValidationError

from src.services.sovren.apis.searcher_services import \
    SovrenSearcherServices
from src.services.sovren.apis.search_job_resume_services import \
    SearchJobResumeServices
from src.services.sovren.apis.get_parsed_jobs_services import GetParsedJobsServices
from src.services.sovren.apis.get_candidate_resume_services import GetCandidateResumeServices
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.helpers.misc_helpers import get_authorized_services

class SearcherServices:
    """
    Searcher services class
    """

    def call_get_parsed_resume(self, request, resume_id: str) -> Dict:
        """
        Get jobs to job list on the basis of services requested
        :param resume_id: SearcherServicesValidations
        :return:
        """
        service_info = get_authorized_services(request)

        try:
            # If Client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    sovren_searcher = SovrenSearcherServices()
                    return sovren_searcher.get_parsed_resume(request, resume_id)
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

    def call_search_job_resume(self, request, data: dict) -> Dict:
        """
        Get jobs to job list on the basis of services requested
        :param data:
        :param request:
        :return:
        """
        service_info = get_authorized_services(request)

        try:
            # If Client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    search_job_resume = SearchJobResumeServices()
                    return search_job_resume.get_search_jobs_resumes(request, data)
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

    def call_get_parsed_jobs(self, request, job_document_id: str) -> Dict:
        """
        Get Parsed Jobs on the basis of services requested
        :param job_id: ParsedJobsValidations
        :return:
        """
        service_info = get_authorized_services(request)

        try:
            # If Client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    get_parsed_jobs = GetParsedJobsServices()
                    return get_parsed_jobs.get_parsed_job(request, job_document_id)
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

    def call_get_candidate_resume(self, request, resume_id: str) -> Dict:
        """
        Get Parsed Jobs on the basis of services requested
        :param job_id: ParsedJobsValidations
        :return:
        """
        service_info = get_authorized_services(request)

        try:
            # If Client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    get_candidate_resume = GetCandidateResumeServices()
                    return get_candidate_resume.get_candidate_resume(request, resume_id)
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
