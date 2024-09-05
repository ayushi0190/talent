# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Scorer routes
@author <rchakraborty@simplifyvms.com>
@author <ankits@simplifyvms.com>
"""

from fastapi import APIRouter,Request
from fastapi import Depends
from fastapi.security.api_key import APIKey
from starlette.responses import JSONResponse

from src.services.common.apis.scorer_services import ScorerServices
from src.services.common.validations.score_by_id_validations import \
    ScoreByIdValidations

from src.utilities.verify import get_api_key
from src.utilities.custom_logging import cust_logger as logger
from src.services.common.helpers.misc_helpers import get_formatted_score_data
import time

scorer_router = APIRouter()


@scorer_router.post('/score/by/id', response_model=ScoreByIdValidations)
async def score_by_id(request: Request, data: ScoreByIdValidations, api_key: APIKey = Depends(get_api_key)) -> JSONResponse:
    """
    Get score based on resume ID and job ID

    """
    scorer = ScorerServices() 
    return JSONResponse(scorer.call_get_score_by_id(request, data))
