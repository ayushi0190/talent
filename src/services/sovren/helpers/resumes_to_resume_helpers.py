# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Miscellaneous helper methods
@author <rchakraborty@simplifyvms.com>
"""
import json
from src.services.sovren.helpers.search_job_resume_helpers import get_candidates_detail_by_id
from src.services.common.config.common_config import common_url_settings

def wrap_matching_resumes(matching_resumes: list, data: dict) -> list:
    """
    Wrap matching jobs
    :param matching_resumes:
    :param data:
    :return:
    """
    result = []
    if len(matching_resumes) > 0:
        for count, ele in enumerate(matching_resumes):
            candidate_data = get_candidates_detail_by_id(ele.get('Id').upper())
            if len(candidate_data) > 0 and \
                    ele.get('Id').lower() != data["resume_id"].lower():
                candidate_data = json.loads(json.dumps(candidate_data))
                if common_url_settings.get("SHARED_BUCKET_NAME") in ele.get('Id').upper().split('-'):
                    pool_category = common_url_settings.get("SHARED_CATEGORY")
                else:
                    pool_category = common_url_settings.get("PRIVATE_CATEGORY")
                result.append(
                    {
                        'Id': ele.get('Id'),
                        'WeightedScore': ele. \
                            get('WeightedScore'),
                        'UnWeightedScore': ele. \
                            get('UnweightedCategoryScores'),
                        'Data': candidate_data,
                        'pool_category': pool_category
                    }
                )
    return result
