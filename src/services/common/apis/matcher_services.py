# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Matcher services
@author <rchakraborty@simplifyvms.com>
@author <sreddy@simplifyvms.com>
"""
from typing import List

from fastapi import status
from pydantic import ValidationError

from src.services.common.helpers.misc_helpers import find_words_exists
from src.services.common.validations.jobs_to_resume_matcher_validations import JobsToResumeMatcherValidations
from src.services.common.validations.matcher_services_validations import \
    MatcherServicesValidations, ResumesToResumeValidations, CandidatesToJobValidations
from src.services.sovren.apis.jobs_to_job_services import JobToJobsServices
from src.services.sovren.apis.resumes_to_resume_services import ResumesToResumeServices
from src.services.sovren.apis.candidates_to_job_services import CandidatesToJobServices
from src.services.sovren.apis.jobs_to_resume_services import JobsToResumeServices
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.helpers.misc_helpers import get_authorized_services


class MatcherServices:
    """
    Matcher services class
    """

    def call_jobs_to_job_matcher(
        self, request, data: MatcherServicesValidations
    ) -> List:
        """
        Get jobs to job list on the basis of services requested
        :param request: Request
        :param data:
        :return:
        """
        service_info = get_authorized_services(request)
        try:
            # If the client info exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    sovren_jobs_to_job = JobToJobsServices()
                    return sovren_jobs_to_job.get_matched_jobs(request, data)
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


    def call_jobs_to_resume_matcher(
        self, request, data: JobsToResumeMatcherValidations
    ) -> List:
        """
        Get jobs to resume list on the basis of services requested
        :param request: Request
        :param data:
        :return:
        """

        service_info = get_authorized_services(request)

        try:
            # If client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    sovren_jobs_to_res = JobsToResumeServices()
                    return sovren_jobs_to_res.get_matched_jobs_to_resume(request, data)
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

    def call_resumes_to_resume_matcher(
        self, request, data: ResumesToResumeValidations
    ) -> List:
        """
        Get Resumes to Resume list on the basis of services requested
        :param exc: RequestValidationError
        :param data:
        :return:
        """
        service_info = get_authorized_services(request)
        try:
            # If client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    sovren_resumes_to_resume = ResumesToResumeServices()
                    return sovren_resumes_to_resume.get_matched_resumes(request, data.dict())
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

    def call_candidates_to_job_matcher(
        self, request, data: CandidatesToJobValidations
    ) -> List:
        """
        Get jobs to job list on the basis of services requested
        :param exc: RequestValidationError
        :param data:
        :return:
        """
        service_info = get_authorized_services(request)
        try:
            # If client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    sovren_candidates_to_job = CandidatesToJobServices()
                    return sovren_candidates_to_job.get_matched_resumes_to_job(request, data.dict())
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
