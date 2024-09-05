common_url_settings = {}
common_url_settings.update(
    {
        "JOB_BOARD_JOB_DETAILS_URL": "https://api.jobboard.zepptalentz.com/job_board_bknd/public/api/pull-jobs",
        "JOB_BOARD_JOB_PARSING_URL": "https://api.jobboard.zepptalentz.com/job_board_bknd/public/api/post-jobdata",
        "JOB_BOARD_AUTHORIZATION": "NNqLko04zssteDeGJUnjLkW0VBLvIpcq7Kaa1wGOTnt",
        "SVMS_PUSH_SCORE_URL": "/index.php/directSourcingCandidates/create",
        "SVMS_PUSH_SCORE_AUTHORIZATION": "VUgZaNfDeQBcrHDbq1RzibDLal914Def",
        "SOVREN_SUBMISSION_SCORE_TO_HIRE": "/api/v1/talentmatcher/sovern-submission-score",
        "OPENING_SUBMISSION_SCORE_TO_HIRE": "/api/v1/talentmatcher/openingio-submission-score",
        "SIMPLIFY_HIRE_SUBMISSION_SCORE_AUTHORIZATION": "113097ae0a543f2fdbcd5146b9334151",
        "RESUME_MAIN_INDEX": "SIMP-R-X-TP-ONE",
        "INTERNAL_BUCKET": "SIMP-R-EX-INTERN",
        "QUERY_DAYS": 184,
        "ONE_MONTH": 30,
        "API_KEY_NAME": "client_id",
        "REDIS_HOST": "tz-dev-redis2.kqnwzf.ng.0001.use1.cache.amazonaws.com",
        "REDIS_PORT": 6379,
        "BROKER_URL": "redis://tz-dev-redis2.kqnwzf.ng.0001.use1.cache.amazonaws.com:6379/0",
        "BROKER_TRANSPORT_OPTIONS": {'visibility_timeout': 3600},
        "CELERY_RESULT_BACKEND": "redis://tz-dev-redis2.kqnwzf.ng.0001.use1.cache.amazonaws.com:6379/0",
        "CELERY_DEFAULT_QUEUE": "talentmatcher",
        "TALENTPOOL_CREATE": "https://api-dev-talentpool.zepptalentz.com/api/v1.0/create-candidate", #update talentpool
        "TALENTPOOL_UPDATE": "https://api-dev-talentpool.zepptalentz.com/api/v1.0/parse-resume", #update talentpool
        # "TALENTPOOL_UPDATE": "http://localhost:9001/api/v1.0/parse-resume",
        # "TALENTPOOL_UPDATE": "http://172.17.0.2:9001/api/v1.0/parse-resume",        # through docker container IP address
        "LIST_JOBS_FROM_JOB_BOARD": "https://api.jobboard.zepptalentz.com/job_board_bknd/public/api/source",
        "LIST_SOURCE_JOBS_FROM_JOB_BOARD": "https://api.jobboard.zepptalentz.com/job_board_bknd/public/api/source-jobs",
        "SOURCE_NAME_FOR_TEST_JOBS": "HIRE",
        "MATCHER_CHECK_LENGTH": 3,
        "LOCATION_API": "http://44.219.40.16:9015/v1/location/distance",
        "TALENTPOOL_CLIENT_REGISTER":"https://api-dev-submission.zepptalentz.com/clients/save", #updated submission
        # "TALENTPOOL_CLIENT_REGISTER":"http://localhost:9002/clients/save",
        # "TALENTPOOL_CLIENT_REGISTER":"http://172.17.0.3:9002/clients/save",         # through docker container IP address

        "SENDGRID_API_KEY": "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",
        "TO_EMAIL":"",
        "FROM_EMAIl":"admin@recruitaicareers.com",
        "CC_EMAIL":["rajkumar.pydev@gmail.com"],
        "SUBJECT":"New Client Registration",
        "MESSAGE":"""Hi Team,<br><br>
A new client has been registered with us. Please use the below details for the new client.<br><br>
Client Name: {}<br>
Client ID: {}<br>
Score: {}<br><br>
Thanks<br>
DirectSource Management""",
        "EMAIL_SUCCESS_MSG":"Email Sent Successfully",
        "EMAIL_FAIL_MSG":"Unable to Send Email",
        "TEST_EMAIL_ACCOUNT":"rajkumar.pydev@gmail.com",
        "PRIVATE_CATEGORY" : "P",
        "SHARED_CATEGORY" : "S",
        "SHARED_BUCKET_NAME" : "INTERN",
        "AUDIT_ALL" : "All",
        "AUDIT_REMOVE_URLS" : ['/data/graph.json','/graph', '/parsing/stats', '/audit/stats',"/api/v1/talentmatcher/sovern-submission-score"],
        "SIMPAI_PARSER_RESUME_URL" :"http://107.20.178.46:9025/v1/parse_resume_base64",
        # "SIMPAI_RESUME_PARSER_URL" :"https://resume-parser.simplify-ai.com/v1/parse_resume_base64",
        "SIMPAI_PARSER_AUTHORIZATION_KEY" :"bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaW1wbGlmeWFpLXByb2R1Y3QiLCJwYXNzd29yZCI6InVzdGVjaCIsImV4cCI6OTA4Mzc2MzUxOH0.kRBmcwI2CLxWtVMLggLfCKjOeCCNFQ2adNF_lLRJbNQ",
        "PDF_EDITOR_API": "https://dev-pdf-edor-api.simplifyapis.com/pdf_append", ## todo
        "SOVREN_SERVICE": "sovren",
        "SIMPAI_SERVICE": "simplifyai",
        "OPENING_SERVICE": "opening",
        "RUN_SIMPAI_IN_BACKGROUND": True,
        "DEFAULT_JOB_CATEGORY": "default"
    }
)
