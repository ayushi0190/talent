# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Matcher routes
@author <rchakraborty@simplifyvms.com>
@author <sreddy@simplifyvms.com>
"""
from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi.security.api_key import APIKey
from starlette.responses import JSONResponse

from src.services.common.apis.matcher_services import MatcherServices
from src.services.common.validations.jobs_to_resume_matcher_validations import \
    JobsToResumeMatcherValidations
from src.services.common.validations.matcher_services_validations import \
    MatcherServicesValidations, ResumesToResumeValidations, CandidatesToJobValidations


from src.utilities.verify import get_api_key

matcher_router = APIRouter()


@matcher_router.post("/match/jobs",
                     response_model=MatcherServicesValidations)
async def match_jobs(
        request: Request, data: MatcherServicesValidations, api_key: APIKey = Depends(get_api_key)
) -> JSONResponse:
    """
    Match jobs against a job
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    jobs_to_job = MatcherServices()
    return JSONResponse(jobs_to_job.call_jobs_to_job_matcher(request, data))

@matcher_router.post("/match/resumes/to/resume",
                     response_model=ResumesToResumeValidations)
async def match_resumes_to_resume(
    request: Request, data: ResumesToResumeValidations, api_key: APIKey = Depends(get_api_key)
) -> JSONResponse:
    """
    Get similar resumes against a resume
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    resumes_to_resume = MatcherServices()
    return JSONResponse(resumes_to_resume.call_resumes_to_resume_matcher(request, data))

@matcher_router.post("/match/candidates/to/job",
                     response_model=CandidatesToJobValidations)
async def match_candidates_to_job(
    request: Request, data: CandidatesToJobValidations, api_key: APIKey = Depends(get_api_key)
) -> JSONResponse:
    """
    Get matching candidates against a job
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    candidates_to_job = MatcherServices()
    return JSONResponse(candidates_to_job.call_candidates_to_job_matcher(request, data))

@matcher_router.post("/match/jobs/resume",
                     response_model=JobsToResumeMatcherValidations)
async def match_jobs_to_resume(
        request: Request, data: JobsToResumeMatcherValidations, api_key: APIKey = Depends(get_api_key)
) -> JSONResponse:
    """
    Get matching jobs against a resume
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    jobs_to_job = MatcherServices()
    return JSONResponse(jobs_to_job.call_jobs_to_resume_matcher(request, data))
