
import logging
import os

from mongoengine import connect
from src.config.config import settings
# env = settings.env
# settings = settings[env]
PATH = os.getcwd()
class DataManager:
    """
    Data manager class
    """

    __instance = None

    def __init__(self):
        """
        Initialize DataManager
        """
        if DataManager.__instance is not None:
            raise Exception(
                "Not possible to create more than one database instance")

        if settings.env in {"PRODUCTION", "AWS_ENV"}:
            # with open('src/cert/global-bundle.pem', "r") as file_buffer:
                # cert = file_buffer.read()
            # uri = f"mongodb://{settings.databases.db_username}:{settings.databases.db_password}@{settings.databases.db_host}:{settings.databases.db_port}/{settings.databases.db_name}?ssl=true&ssl_ca_certs={PATH}/src/cert/global-bundle.pem&retryWrites=false" # pylint: disable=line-too-long
            uri = f"mongodb://{settings[settings.env].DATABASES.DB_USERNAME}:{settings[settings.env].DATABASES.DB_PASSWORD}@{settings[settings.env].DATABASES.DB_HOST}:{settings[settings.env].DATABASES.DB_PORT}/{settings[settings.env].DATABASES.DB_NAME}?ssl=true&ssl_ca_certs={PATH}/src/cert/global-bundle.pem&retryWrites=false"  # pylint: disable=line-too-long
            logging.warning("MONGO_URI : ", uri)
        else:
            uri = f"mongodb://{settings[settings.env].databases.db_host}:{settings[settings.env].databases.db_port}/{settings[settings.env].databases.db_name}"  # pylint: disable=line-too-long
        DataManager.__instance = connect(host=uri)

    @classmethod
    def get_instance(cls):
        """
        Get the instance of DataManager
        :return:
        """
        if DataManager.__instance is None:
            DataManager()
            if DataManager.__instance is None:
                raise Exception("uri not correct")
        return DataManager.__instance
