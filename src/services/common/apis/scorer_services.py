"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Scorer routes
@author <ankits@simplifyvms.com>
"""

from typing import Dict

from fastapi import status
from pydantic import ValidationError
from src.services.common.validations.score_by_id_validations import \
    ScoreByIdValidations
from src.services.sovren.apis.res_to_job_score_services import \
    ResToJobScoreServices
from src.services.common.helpers.misc_helpers import get_authorized_services
from src.services.simpai.apis.scorer_services import \
    SimpResToJobScoreServices
from src.services.common.config.common_config import common_url_settings
from src.utilities.tasks import score_job_resume_simpai

class ScorerServices:
    """
    Scorer services class
    """
    def __init__(self):
        self.score_parsed_resp = None
        self.background = True

    def call_get_score_by_id(self, request, data: ScoreByIdValidations) -> Dict:
        """
        Get Score
        :param request:
        :param data:
        :return:
        """
        service_info = get_authorized_services(request)
        client_id = request.headers["client_id"]
        try:
            # If the client info exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov and data.parse_with.lower() \
                == common_url_settings.get("SOVREN_SERVICE"):
                    scorer = ResToJobScoreServices()
                    result = scorer.get_score(request, data.resume_id,
                                              data.job_id, data.job_category,
                                              data.category_weights)
                    self.score_parsed_resp = scorer.score_parsed_resp
                    '''call simpai matcher in background '''
                    if common_url_settings.get("RUN_SIMPAI_IN_BACKGROUND") \
                    and self.background:
                        score_job_resume_simpai.delay(client_id,
                                data.resume_id, data.job_id, data.job_category)
                        pass

                    return result
                # If selected tool is Opening
                if service_info.tol_ope and data.parse_with.lower() \
                == common_url_settings.get("OPENING_SERVICE"):
                    pass
                # If selected tool is Simplifyai
                if service_info.tol_sim and data.parse_with.lower() \
                == common_url_settings.get("SIMPAI_SERVICE"):
                    scorer = SimpResToJobScoreServices()
                    result = scorer.get_score(client_id, data.resume_id,
                                              data.job_id, data.job_category)
                    self.score_parsed_resp = scorer.score_parsed_resp
                    return result
                    pass
            else:
                return dict({
                    'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'message': "No Client Information Exist"
                })

        except ValidationError as exc:
            return dict({
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': exc.errors()
            })
