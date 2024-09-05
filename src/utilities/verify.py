# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Verify JWT token related tasks
@author <AnujY@simplifyvms.com>
@author <sreddy@simplifyvms.com>
"""

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyHeader, Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from src.admin.helpers.admin_helpers import user_serv_perm, find_field_name
from src.admin.config.admin_configs import common_adm_settings
from src.db.crud.admin.auth_schema import AuthSchema
from src.services.common.config.common_config import common_url_settings
from src.utilities.token import JWTToken
from src.utilities.type import ResponseBody
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from datetime import datetime, timedelta

jwt_key_header = APIKeyHeader(name=common_url_settings.get("API_KEY_NAME"),
                              auto_error=False)


def get_api_key(request: Request,
                api_key_header: str = Security(jwt_key_header),
                ) -> bool:
    """
    Get API Key
    :param api_key_query:
    :param api_key_header:
    :return:
    """

    if api_key_header is not None:
        return validate_request(request, api_key_header)
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=ResponseBody(
                code=HTTP_401_UNAUTHORIZED,
                data=None,
                error="Could not validate credentials").dict()
        )


def validate_client(request, client_id: str) -> bool:
    """ function used to verify client is valid or not """
    active_model = AuthSchema()
    user_data = active_model.get(client_id)
    if user_data:
        if user_data.auth_type != common_adm_settings.get("ADMIN_AUTH_TYPE"):
            requested_url = request.url.path
            val_con_per = validate_contract_period(request, client_id)
            if not val_con_per:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN,
                    detail=ResponseBody(
                        code=HTTP_403_FORBIDDEN,
                        data=None,
                        error="Client contract period is expired").dict())
            return validate_service(request, user_data.clt_id, requested_url)
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=ResponseBody(
                code=HTTP_403_FORBIDDEN,
                data=None,
                error="you are not authorized to make request").dict())


def validate_contract_period(request, client_id: str) -> bool:
    """
    Function used to check contract period expires for the client
    :param request:
    :param client_id:
    :return:
    """

    user_data = CltRegSchema().get_client_info(request, client_id)
    if user_data:
        no_of_days = (datetime.utcnow().date() - user_data.reg_dt.date()).days
        if user_data.cont_prd > no_of_days:
            return True
        else:
            return False
    return False


def validate_service(request, clt_id: str, service_name: str) -> bool:
    """ function used to verify client service access permission """
    field = find_field_name(service_name)
    allow_pms = user_serv_perm(request, clt_id, field)
    if allow_pms is None or allow_pms is False:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=ResponseBody(
                code=HTTP_403_FORBIDDEN,
                data=None,
                error="you have not permission to access this service").dict())
    else:
        return clt_id


def validate_request(request, api_key: str) -> bool:
    """
    Validate request
    :param api_key:
    :return:
    """
    jwt_object = JWTToken()
    active_model = AuthSchema()
    user_data = active_model.get(api_key)
    api_key_check = None
    if user_data is not None:
        api_key_check = user_data.token
    _payload: dict = jwt_object.validate_token(api_key_check)
    if _payload.get('clt_id'):
        return validate_client(request, api_key)

def service_url_check(request, clt_id: str, service_name: str) -> bool:
    """ function used to verify client service access permission """
    field = find_field_name(service_name)
    allow_pms = user_serv_perm(request, clt_id, field)
    if allow_pms is None or allow_pms is False:
        return False
    else:
        return clt_id
