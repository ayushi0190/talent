# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Parser services
@author <rchakraborty@simplifyvms.com>
"""
import json
from typing import Dict
from datetime import datetime
import arrow
from fastapi import status
from pydantic import ValidationError
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from src.db.crud.common.score_test import ScoreTest


class ScoreTestServices:
    """
    Score Test services class
    """

    def call_get_score_test(self, request, data: dict) -> Dict:
        """
        Parse job
        :param request:
        :param data:
        :return:
        """
        request.app.logger.info("Requests  for submission score test: %s" % request.headers)
        try:
            result = {}
            db_to_save = ScoreTest()
            ret = db_to_save.add_score(request, data)
            if ret:
                result.update({
                    "message": "Score Received from Submission"
                })
            else:
                result.update({
                    "message": "Error in Saving Score from Submission"
                })
            return result

        except ValidationError as exc:
            return dict({
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': exc.errors()
            })
