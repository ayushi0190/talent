# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Admin routes
@author <rchakraborty@simplifyvms.com>
"""
from fastapi import APIRouter, Request
from starlette.responses import JSONResponse

from src.admin.validations.client_registration_validations import ClientRegistrationValidations
from src.admin.apis.admin_services import AdminServices


config_router = APIRouter()


@config_router.post("/register/client",
                    response_model=ClientRegistrationValidations)
async def register_client(
        request: Request, data: ClientRegistrationValidations
) -> JSONResponse:
    """ get result """
    admin_services = AdminServices()
    return JSONResponse(admin_services.register_client(request, data))
