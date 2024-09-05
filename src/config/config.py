# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
file help to setup settings.yaml file
@author <anujy@simplifyvms.com>
"""
import os
from dynaconf import Dynaconf
import src.config.settings as aws_settings
settings = Dynaconf(
    settings_files=['settings.yaml'],
)
if settings.env == "PRODUCTION":
    env = os.getenv("BUILD_ENV")
    secret_aws: str = settings[settings.get('env')].get(
        'aws').get('aws_secret_name')
    print(secret_aws)
    print(env)
    aws_secret = aws_settings.get_secret(env, secret_aws)
    prod = settings.production
    prod['AWS']['SOVREN_ACCOUNT_ID'] = aws_secret.get("SOVREN_ACCOUNT_ID")
    prod['AWS']['SOVREN_ACCOUNT_SERVICE_KEY'] = aws_secret.get("SOVREN_ACCOUNT_SERVICE_KEY")
    prod['DATABASES']['DB_ENGINE'] = aws_secret.get("docdbEngine")
    prod['DATABASES']['DB_HOST'] = aws_secret.get("docdbHost")
    prod['DATABASES']['DB_PORT'] = aws_secret.get("docdbPort")
    prod['DATABASES']['DB_USERNAME'] = aws_secret.get("docdbUserName")
    prod['DATABASES']['DB_PASSWORD'] = aws_secret.get("docdbPassword")
    prod['DATABASES']['DB_NAME'] = aws_secret.get("docdbName")
    prod['DATABASES']['DB_CLUSTERIDENTIFIER'] = aws_secret.get(
        "docdbClusterIdentifier")
    prod['AWS']['REDIS_HOST'] = aws_secret.get("redisHost")
    prod['AWS']['REDIS_PORT'] = aws_secret.get("redisPort")
    prod['AWS']['REDIS_PASSWORD'] = aws_secret.get("redisPassword")
    host = aws_secret.get("sesHost")
    port = aws_secret.get("sesPort")
    user = aws_secret.get("sesUsername")
    password = aws_secret.get("sesPassword")
    #print(prod)
host = "ses-smtp-user.20230424-021212"
port = "2465"
user = "AKIATRC54W7TWA3VXXXL"
password = "BLOUtapfzKe/kdjIZKYoZnmCl4sNLR04qVKsGGOeI5m7"
