from fastapi import Request, APIRouter
from starlette.responses import JSONResponse

from src.services.common.apis.score_test_services import ScoreTestServices
from src.services.common.config import common_config
import time

score_test_router = APIRouter()

@score_test_router.post( common_config.common_url_settings.get("SOVREN_SUBMISSION_SCORE_TO_HIRE"))
async def score_test(request: Request, data: dict ) -> JSONResponse:
    """
    Test Score
    :param request:
    :param data:
    :return:
    """
    score_test = ScoreTestServices()

    return JSONResponse(score_test.call_get_score_test(request, data))
