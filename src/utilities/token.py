# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Token generation and validation logic
@author <AnujY@simplifyvms.com>
"""

import jwt
from fastapi import HTTPException

from src.utilities.type import ResponseBody
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN


class JWTToken:
    """
    Token decode and encode function's
    """
    def _init_(self):
        """
        Initialize
        """
        self.__secret_private: str = """testing private jwt
                                """
        self.__secret_public: str = """testing private jwt
                               """

    def generate_token(self, payload: dict) -> str:
        """
        Generate token
        :param payload:
        :return:
        """
        try:
            token: str = jwt.encode(
                payload, "testing private jwt", algorithm="HS256")
            return token
        except Exception as err:
            print("Error while generating new token", {"error": err})
            raise HTTPException(
                status_code=403,
                detail=ResponseBody(
                    data=None, error="Error while generating new token"
                ).dict(),
            ) from err

    def validate_token(self, jwt_string: str) -> dict:
        """
        Validate token
        :param jwt_string:
        :return:
        """
        try:
            payload: dict = jwt.decode(
                jwt_string, "testing private jwt", algorithms=['HS256']
            )
            return payload
        except jwt.exceptions.ExpiredSignatureError as err:
            print("Token expired", {"error": err})
            raise HTTPException(
                status_code=401,
                detail=ResponseBody(
                    code=HTTP_401_UNAUTHORIZED,
                    data=None, error="Token expired").dict(),
            ) from err
        except Exception as err:
            print("Error while verifying token", {"error": err})
            raise HTTPException(
                status_code=401,
                detail=ResponseBody(
                    code=HTTP_401_UNAUTHORIZED,
                    data=None, error="Error while verifying token"
                ).dict(),
            ) from err
