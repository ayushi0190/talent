
from datetime import datetime

from mongoengine.errors import SaveConditionError, ValidationError

from src.db.config.db import DataManager
from src.db.models.admin.auth import AuthModel

DataManager.get_instance()


class AuthSchema:
    """ Authentication Creation """

    def add(self, data: dict) -> bool:
        """
        Add record
        :param data: dict
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = AuthModel.objects(clt_id=data.get('clt_id')).first()
            if existing_record is None:
                new_record = AuthModel(
                    name=data.get('name'),
                    clt_id=data.get('clt_id'),
                    auth_type=data.get('auth_type'),
                    token=data.get('token')
                )
                if new_record.save():
                    return True
            return False
        except (SaveConditionError, ValidationError):
            return False

    def get(self, clt_id: str) -> dict:
        """
        Get record
        :param clt_id:
        :return:
        """
        try:
            return AuthModel.objects(clt_id=clt_id).first()
        except Exception as es:
            return False

    def update_auth_info(self, data: dict) -> bool:
        """
        Update authentication information
        :param data:
        :return:
        """
        try:
            existing_record = AuthModel.objects(clt_id=data.get('clt_id'))
            if existing_record:
                data.update({
                    "updated_at": datetime.utcnow()
                })
                if existing_record.update(**data):
                    return True
            return False
        except (SaveConditionError, ValidationError):
            return False
