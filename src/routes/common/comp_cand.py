"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Compare Candidate Routes
@author <ankits@simplifyvms.com>
"""

from fastapi import APIRouter,Request
from fastapi import Depends
from fastapi.security.api_key import APIKey
from starlette.responses import JSONResponse

from src.services.common.apis.comp_cand_services import CompCandServices
from src.services.sovren.interfaces.comp_cand_interface import \
    CompareCandidateInput

from src.utilities.verify import get_api_key

comp_cand_router = APIRouter()


@comp_cand_router.post('/compare/candidates')
async def compare_candidates(request: Request, data: CompareCandidateInput, api_key: APIKey = Depends(get_api_key)) -> JSONResponse:
    """
    Compare Candidates against a JOB
    """
    comp_cand_to_job = CompCandServices()
    return comp_cand_to_job.call_comp_cand_to_job(request,data)
