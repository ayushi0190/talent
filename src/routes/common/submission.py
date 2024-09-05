from fastapi import Request, APIRouter
from fastapi import Depends
from fastapi.security.api_key import APIKey

from starlette.responses import JSONResponse

from src.services.common.apis.parser_services import ParserServices
from src.services.common.validations.submission_validations import (SubmissionValidations)

from src.utilities.verify import get_api_key

submission_router = APIRouter()


@submission_router.post('/submission', response_model=SubmissionValidations)
async def submission(request: Request, data: SubmissionValidations,
                                api_key: APIKey = Depends(get_api_key)) -> JSONResponse:
    """
    Parse Submission sends an generated score based on parse resume and parse job
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    parser = ParserServices()
    return JSONResponse(parser.call_parse_submission(request, data))
