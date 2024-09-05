
import json
import boto3
from botocore.exceptions import ClientError
import logging

boto3.set_stream_logger('botocore', logging.INFO)

def get_secret(region: str, secret_aws: str):
    """ function help to get aws secret manager """
    #secret_name = f"{env}/{secret_aws}"
    secret_name = secret_aws
    region_name = region

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        logging.warning("secret_name {}".format(secret_name))
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name

        )
    except ClientError as err:
        if err.response['Error']['Code'] == 'ResourceNotFoundException':
            logging.warning("The requested secret " + secret_name + " was not found")
        elif err.response['Error']['Code'] == 'InvalidRequestException':
            logging.warning("The request was invalid due to:", err)
        elif err.response['Error']['Code'] == 'InvalidParameterException':
            logging.warning("The request had invalid params:", err)
    else:
        if 'SecretString' in get_secret_value_response:
            secret = json.loads(get_secret_value_response['SecretString'])
            return secret