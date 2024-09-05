# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Miscellaneous helper methods
@author <rchakraborty@simplifyvms.com>
"""


def wrap_matching_jobs(matching_jobs: list) -> list:
    """
    Wrap matching jobs
    :param matching_jobs: Dictionary
    :return:
    """
    result = []
    if len(matching_jobs) is not None:
        for _count, ele in enumerate(matching_jobs):
            searched_job_id = ele.get("Id").split("-")
            modified_job_id = (
                    searched_job_id[0].upper()
                    + "-"
                    + searched_job_id[1].upper()
                    + "-"
                    + searched_job_id[2].upper()
                    + "-"
                    + searched_job_id[3].upper()
                    + "-"
                    + searched_job_id[4]
                    + "-"
                    + searched_job_id[5]
            )
            result.append(
                {
                    "Id": modified_job_id,
                    "WeightedScore": ele.get("WeightedScore"),
                    "UnweightedCategoryScores": ele.get("UnweightedCategoryScores"),
                }
            )
    return result


def jobs_to_job_filters(payload: dict, data: dict) -> dict:
    """
    Jobs to job filters for Payload
    :param payload:
    :param data:
    :return:
    """
    if data.Skills:
        if data.Skills[0] and data.Skills[0] != 'string':
            payload['FilterCriteria']['Skills'] = []
            for i in data.Skills:
                payload['FilterCriteria']['Skills'].append(
                    {'SkillName': ''. \
                        join(e for e in i if e.isalnum() or e.isspace())})

    return payload
