# -*- coding: utf-8 -*-

simpai_url_settings = {}
simpai_url_settings.update(
    {
        # https://dev-jobboard.simplifyapis.com/ziprecruiter/v2.0/jobs
        # "SIMPAI_RESUME_PARSER_URL": "https://dev-service.simplifyapis.com/v1/parse_resume_base64",
        # "SIMPAI_RESUME_PARSER_URL" :"https://dev-service.simplifyapis.com/v1/parse_resume",
        "SIMPAI_RESUME_PARSER_URL" :"https://resume-parser.simplify-ai.com/v1/parse_resume_base64",
        "SIMPAI_RESUME_PARSER_AUTHORIZATION_KEY": "Token MTQ4NjE1BWRC1S4XzE3Ml85XZXN1bWU",

        "SIMPAI_MATCHER_URL": "https://job-maher.simplify-ai.com/v1/matcher/",
        "SIMPAI_MATCHER_AUTH_TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaW1wYWktbWF0Y2hpbmctYXBpIiwiZXhwIjoxNjUwMTAxNjM4fQ.leVaffxd0cQuExY2B1g7p-AMWlAGv6i0W7ua-t43MX0",
        # "SIMPAI_JOB_PARSER_URL": "https://dev-job-parser.simplifyapis.com/api/v1/parse_job",
        # "SIMPAI_JOB_PARSER_URL_old": "https://dev-parser.simplify-ai.com/job_parser/v1/parse_job",
        "SIMPAI_JOB_PARSER_URL": "https://job-parser.simplify-ai.com/api/v1/parse_jd",
        "SIMPAI_JOB_PARSER_URL_old": "https://dev-parser.simplify-ai.com/job_parser/parse_jd",
        "SIMPAI_JOB_PARSER_AUTH_TOKEN": "MTQ4NjE1BWRC1S4XzE3Ml85XZXN1bWU",

        "SIMPAI_JOB_NORM_URL": "https://dev-job-norm-api.simplifyapis.com/normalize_job",
        "SIMPAI_JOB_NORM_AUTH_TOKEN": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaW1wYWktam9iLW5vcm0tYXBpIiwiZXhwIjoxNjUwMTAxNTM3fQ.pUyHN7rsfdOU8LknEVyxpPwv4srQqv9IfW41shiW2dA",
        "SIMPAI_RESUME_NORM_URL": "https://resume-norm-api.simplifyapis.com/resume/normalization",
        # "SIMPAI_RESUME_NORM_URL": "https://resume-norm-api.simplifyapis.com/resume/normalization",


        "CATEGORY1": "SKILLS",
        "WEIGHT1": "0.75",
        "CATEGORY2": "INDUSTRIES",
        "WEIGHT2": "0.25",
        "INDEX_TYPE_JOB": "Job",
        "INDEX_TYPE_RESUME": "Resume",
        "RESUME_INDEX": 'SIMP-R-EX',
        "SIMPAI_SERVICE": "simplifyai",
    }
)