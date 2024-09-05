# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Parser routes
@author <rchakraborty@simplifyvms.com>
"""
from fastapi import Request, APIRouter
from fastapi import Depends
from fastapi.security.api_key import APIKey

from starlette.responses import JSONResponse

from src.services.common.apis.parser_services import ParserServices
from src.services.common.apis.job_parser_services import JobParserServices
from src.services.common.apis.resume_parser_services import ResumeParserServices
from src.services.common.helpers.misc_helpers import get_formatted_job_data, get_formatted_resume
from src.services.common.validations.job_parse_by_description_validations import (JobParseByDescriptionValidations)
from src.services.common.validations.job_parse_by_id_validations import (JobParseByIdValidations)
from src.services.common.validations.parse_resume_validations import ParseResumeValidations
from src.services.common.validations.submission_validations import (SubmissionValidations)
from src.services.common.validations.delete_job_validations import DeleteJobValidations
from src.services.common.validations.delete_resume_validations import DeleteResumeValidations
from src.services.common.validations.parse_profile_validations import ParseProfileValidations

from src.utilities.verify import get_api_key

parser_router = APIRouter()


@parser_router.post('/parse/job/by/id', response_model=JobParseByIdValidations)
async def parse_job_by_id(request: Request, data: JobParseByIdValidations,
                              api_key: APIKey = Depends(get_api_key)) -> JSONResponse:
    """
    Parse job by Id with any services like sovren or simpai or opening
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    job_parser = JobParserServices()
    return JSONResponse(job_parser.call_parse_job(request, data))


@parser_router.post('/parse/job/by/description', response_model=JobParseByDescriptionValidations)
async def parse_job_by_description(request: Request, data: JobParseByDescriptionValidations,
                                api_key: APIKey = Depends(get_api_key)) -> JSONResponse:
    """
    Parse job by description with any services like sovren or simpai or opening
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    parser = ParserServices()
    return JSONResponse(parser.call_get_parsed_job_by_description(request, data))


@parser_router.post('/parse/resume', response_model=ParseResumeValidations)
async def parse_resume(request: Request, data: ParseResumeValidations,
                           api_key: APIKey = Depends(get_api_key)) -> JSONResponse:
    """
    Routes to call Parse Resume
    :param request: for logging
    :param data: document_as_base_64_string
    :return: JSON output
    """
    resume_parser = ResumeParserServices()
    return JSONResponse(resume_parser.call_parse_resume(request, data))


@parser_router.post('/delete/resume', response_model=DeleteResumeValidations)
async def delete_resume(request: Request, data: DeleteResumeValidations,
                           api_key: APIKey = Depends(get_api_key)) -> JSONResponse:
    """
    Routes to call Delete Resume
    :param request: for logging
    :param data: index_id
    :param data: resume_id
    :return: JSON output
    """
    parser = ResumeParserServices()
    return JSONResponse(parser.call_delete_resume(request, data))


@parser_router.post('/delete/job', response_model=DeleteJobValidations)
async def delete_job(request: Request, data: DeleteJobValidations,
                           api_key: APIKey = Depends(get_api_key)) -> JSONResponse:
    """
    Routes to call Delete Job
    :param request: for logging
    :param data: index_id
    :param data: resume_id
    :return: JSON output
    """
    parser = ParserServices()
    return JSONResponse(parser.call_delete_job(request, data))


@parser_router.post('/parse/profile', response_model=ParseProfileValidations)
async def parse_profile(request: Request, data: ParseProfileValidations,
                              api_key: APIKey = Depends(get_api_key)) -> JSONResponse:
    """
    Parse job by Id with any services like sovren or simpai or opening
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    resume_parser = ResumeParserServices()
    return JSONResponse(resume_parser.call_parse_profile(request, data))
