# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Admin routes
@author <rchakraborty@simplifyvms.com>
"""
from fastapi import APIRouter, Request
from fastapi import Depends
from fastapi.security.api_key import APIKey
from starlette.responses import JSONResponse

from src.admin.validations.client_category_weights_validations import ClientCategoryWeightValidations
from src.admin.apis.profile_services import ProfileServices
from src.utilities.verify import get_api_key


profile_router = APIRouter()


@profile_router.post("/profile/category/weights",
                     response_model=ClientCategoryWeightValidations)
async def register_client(
        request: Request, data: ClientCategoryWeightValidations, api_key: APIKey = Depends(get_api_key)
) -> JSONResponse:
    """ get result """
    profile_services = ProfileServices()
    return JSONResponse(profile_services.client_category_weights(request, data))
