# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Celery Initiation
@author <ankits@simplifyvms.com>
"""

import logging
import os
from dynaconf import Dynaconf
import urllib
from urllib.parse import quote
import ssl
from celery import Celery
from src.services.common.config import common_config
import src.config.settings as aws_settings


settings = Dynaconf(
    settings_files=['settings.yaml'],
)
print("CELERY_EN", settings.env)

# celery_env: str = ''

if settings.env == "PRODUCTION":
    logging.warning(f"{settings.env} settings : {settings}")
    env = os.getenv("BUILD_ENV")
    secret_name = os.getenv("SECRET_NAME")
    region = os.getenv("REGION")
    #secret_aws: str = settings[settings.get('env')].get('aws').get('aws_secret_name')
    print("celery secret_name {} ".format(secret_name))
    aws_secret = aws_settings.get_secret(region, secret_name)
    # celery_env = settings[settings.get('env')].get('CELERY_ENV')
    logging.warning("CELERY_RESULT_BACKEND : ", f'rediss://:{aws_secret.get("redisPassword")}@{aws_secret.get("redisHost")}:{aws_secret.get("redisPort")}')
    logging.warning("BROKER_URL : ", f'rediss://:{aws_secret.get("redisPassword")}@{aws_secret.get("redisHost")}:{aws_secret.get("redisPort")}')

    CELERY_RESULT_BACKEND = f'rediss://:{aws_secret.get("redisPassword")}@{aws_secret.get("redisHost")}:{aws_secret.get("redisPort")}'
    BROKER_URL = f'rediss://:{aws_secret.get("redisPassword")}@{aws_secret.get("redisHost")}:{aws_secret.get("redisPort")}'
    BROKER_USE_SSL = {
        'ssl_cert_reqs': ssl.CERT_NONE
    }
    REDIS_USE_SSL = {
        'ssl_cert_reqs': ssl.CERT_NONE
    }

elif settings.env == "AWS_ENV":
    logging.warning(f"{settings.env} settings : {settings}")

    # CELERY_RESULT_BACKEND = f'redis://:{urllib.parse.quote_plus(settings[settings.env].REDIS_PASSWORD)}@{settings[settings.env].REDIS_HOST}:{settings[settings.env].REDIS_PORT}'
    # BROKER_URL = f'redis://:{urllib.parse.quote_plus(settings[settings.env].REDIS_PASSWORD)}@{settings[settings.env].REDIS_HOST}:{settings[settings.env].REDIS_PORT}'

    # redis connect without pwd
    CELERY_RESULT_BACKEND = f'redis://{settings[settings.env].REDIS_HOST}:{settings[settings.env].REDIS_PORT}'
    BROKER_URL = f'redis://{settings[settings.env].REDIS_HOST}:{settings[settings.env].REDIS_PORT}'

    # redis connect with pwd
    # CELERY_RESULT_BACKEND = f'rediss://{settings[settings.env].REDIS_PASSWORD}@{settings[settings.env].REDIS_HOST}:{settings[settings.env].REDIS_PORT}'
    # BROKER_URL = f'rediss://{settings[settings.env].REDIS_PASSWORD}@{settings[settings.env].REDIS_HOST}:{settings[settings.env].REDIS_PORT}'

    logging.warning("CELERY_RESULT_BACKEND : ", CELERY_RESULT_BACKEND)
    logging.warning("BROKER_URL : ", BROKER_URL)
    BROKER_USE_SSL = None
    REDIS_USE_SSL = None

    # Use in SSL/TLS connection
    # BROKER_USE_SSL = {
    #     'ssl_cert_reqs': ssl.CERT_NONE,
    #     'ssl': False
    # }
    # REDIS_USE_SSL = {
    #     'ssl_cert_reqs': ssl.CERT_NONE,
    #     'ssl': False
    # }
else:
    logging.warning(f"{settings.env} settings : {settings}")
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # BROKER_URL = 'pyamqp://guest@localhost//'
    BROKER_URL = 'redis://localhost:6379/0'
    BROKER_USE_SSL = None
    REDIS_USE_SSL = None

# Create the celery app and get the logger
#celery_app = Celery('talentmatcher', broker=common_config.common_url_settings.get("BROKER_URL"),\
#                     backend=common_config.common_url_settings.get("CELERY_RESULT_BACKEND"))

#print("CELERY_RESULT_BACKEND", CELERY_RESULT_BACKEND)
#print("BROKER_URL:  " ,BROKER_URL)
#print("BROKER_USE_SSL: " , BROKER_USE_SSL)
#print("REDIS_USE_SSL:  " ,REDIS_USE_SSL)

celery_app = Celery('tasks', backend=CELERY_RESULT_BACKEND, broker=BROKER_URL, broker_use_ssl=BROKER_USE_SSL,
             redis_backend_use_ssl=REDIS_USE_SSL)


celery_app.conf.task_default_queue = 'matcher_recruitai'
celery_app.autodiscover_tasks(['src.utilities.tasks'])