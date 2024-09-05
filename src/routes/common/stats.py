# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Stats Routes
@author <rchakraborty@simplifyvms.com>
@author <sreddy@simplifyvms.com>
"""
from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi.security.api_key import APIKey
from starlette.responses import JSONResponse

from src.services.common.apis.parsing_stats_services import ParsingStatsServices, AuditStatsServices
from src.services.common.validations.parsing_stats_validations import ParsingStatsValidations, AuditStatsValidations

from src.utilities.verify import get_api_key

stats_router = APIRouter()


@stats_router.post("/parsing/stats",
                     response_model=ParsingStatsValidations)
async def parsing_stats(
        request: Request, data: ParsingStatsValidations, api_key: APIKey = Depends(get_api_key)
) -> JSONResponse:
    """
    Prasing Stats Information
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    parsing_stats_service = ParsingStatsServices()
    return JSONResponse(parsing_stats_service.call_parsing_stats(request, data))

@stats_router.post("/audit/stats",
                     response_model=AuditStatsValidations)
async def audit_stats(
        request: Request, data: AuditStatsValidations, api_key: APIKey = Depends(get_api_key)
) -> JSONResponse:
    """
    Audit Stats Information
    :param request:
    :param data:
    :param api_key:
    :return:
    """
    audit_stats_service = AuditStatsServices()
    return JSONResponse(audit_stats_service.call_audit_stats(request, data))
