# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Searcher routes
@author <rchakraborty@simplifyvms.com>
@author <sreddy@simplifyvms.com>
@author <satya@simplifyvms.com>
"""
from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi.security.api_key import APIKey
from starlette.responses import JSONResponse

from src.services.common.apis.searcher_services import SearcherServices
from src.services.common.validations.searcher_services_validations import \
    SearcherServicesValidations, GetCandidateResumeValidations, ParsedJobsValidations, \
    SearchJobsResumesValidations

from src.utilities.verify import get_api_key

searcher_router = APIRouter()


@searcher_router.post('/search/parsed/resume',
                      response_model=SearcherServicesValidations)
async def search_parsed_resume(request: Request, data: SearcherServicesValidations,
                      api_key: APIKey = Depends(get_api_key)) -> JSONResponse:
    """
    Get parsed resume
    :param data:
    :param api_key:
    :return:
    """
    search_service = SearcherServices()
    return JSONResponse(search_service.call_get_parsed_resume(request, data.resume_id))


@searcher_router.post('/search/candidate/resume', response_model=GetCandidateResumeValidations)
async def search_candidate_resume(
        request: Request, data: GetCandidateResumeValidations,
        api_key: APIKey = Depends(get_api_key)) -> JSONResponse:
    """
    Get candidate resume
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    candidate_resume_service = SearcherServices()
    return JSONResponse(candidate_resume_service.call_get_candidate_resume(request, data.resume_id))


@searcher_router.post('/search/parsed/jobs', response_model=ParsedJobsValidations)
async def search_parsed_jobs(
        request: Request, data: ParsedJobsValidations,
        api_key: APIKey = Depends(get_api_key)) -> JSONResponse:
    """
    Get parsed job information
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    parsed_jobs_service = SearcherServices()
    return JSONResponse(parsed_jobs_service.call_get_parsed_jobs(request, data.job_document_id))


@searcher_router.post('/search/jobs/resumes',
                      response_model=SearchJobsResumesValidations)
async def search_jobs_resumes(
        request: Request, data: SearchJobsResumesValidations,
        api_key: APIKey = Depends(get_api_key)) -> JSONResponse:
    """
    Search jobs and resumes
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    search_jobs_resumes = SearcherServices()
    return JSONResponse(search_jobs_resumes.call_search_job_resume(request, data.dict()))
