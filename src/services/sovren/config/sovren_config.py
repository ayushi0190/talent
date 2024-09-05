# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Add configurations for accessing Sovren API's
@author <rchakraborty@simplifyvms.com>
"""
sovren_url_settings = {}
sovren_url_settings.update(
    {
        "SOVREN_DOCUMENT_MATCHER_URL": "https://rest.resumeparsing.com/v9/matcher/documents",
        "SOVREN_MATCH_DOCUMENT_BY_ID_URL": "https://rest.resumeparsing.com/v9/matcher/indexes/",
        "SOVREN_MATCH_DOCUMENT_BY_CRITERIA_URL": "https://rest.resumeparsing.com/v9/matcher/criteria",
        "SOVREN_SEARCH_URL": "https://rest.resumeparsing.com/v9/searcher",
        "SOVREN_BIMETRIC_SCORE_URL": "https://rest.resumeparsing.com/v9/scorer/bimetric",
        "SOVREN_CREATE_INDEX_URL": "https://rest.resumeparsing.com/v9/index/",
        "SOVREN_GET_INDEX_URL": "https://rest.resumeparsing.com/v9/index",
        "SOVREN_PARSE_RESUME_URL": "https://rest.resumeparsing.com/v9/parser/resume",
        "SOVREN_PARSE_JOB_ORDER_URL": "https://rest.resumeparsing.com/v9/parser/joborder",
        "CATEGORY1": "SKILLS",
        "WEIGHT1" : "0.75",
        "CATEGORY2": "INDUSTRIES",
        "WEIGHT2" : "0.25",
        "INDEX_TYPE_JOB": "Job",
        "INDEX_TYPE_RESUME": "Resume",
        "RESUME_INDEX": 'SIMP-R-EX',
        "SOVREN_SERVICE": "sovren",
        "SOVREN_ACCOUNT_ID": "15823295",
        "SOVREN_ACCOUNT_SERVICE_KEY": "FRpGQFZv32KmMMYGMjq5hDka78PtgVoEkKTsFzTC"
    }
)
