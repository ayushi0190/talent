# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Database related operations for model ResMapperModel
@author <rchakraborty@simplifyvms.com>
"""
from typing import Union, Any

from mongoengine.errors import SaveConditionError, ValidationError, LookUpError

from src.db.config.db import DataManager

from src.db.models.sovren.res_maper import ResMapperModel

DataManager.get_instance()


class ResMapperSchema:
    """ Resume mapper """

    def add(self, res_idx_id: str, res_doc_id: str, res_id: str) -> bool:
        """
        Add record
        :param res_id: String
        :param res_doc_id: String
        :param res_idx_id: String
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = ResMapperModel.objects(res_id=res_id).first()
            new_record = None
            if existing_record is None:
                new_record = ResMapperModel(
                    res_idx_id=res_idx_id,
                    res_id=res_id,
                    res_doc_id=res_doc_id
                )
            if new_record:
                if new_record.save():
                    return True
                return False
            return False
        except (SaveConditionError, ValidationError):
            return False

    def get(self, res_doc_id: str, res_idx_id: str) -> Union[bool, Any]:
        """
        Get the record by resume_id
        :param res_idx_id: String
        :param res_doc_id: String
        :return:
        """
        try:
            return ResMapperModel.objects(res_doc_id=res_doc_id, res_idx_id=res_idx_id).first()
        except LookUpError:
            return False

    def update(self, res_doc_id: str, res_idx_id: str,
               res_id: str, is_dup: bool) -> dict:
        """
        Update record
        :param res_doc_id:
        :param res_idx_id:
        :param res_id:
        :param is_dup:
        :return:
        """
        try:
            existing_record = ResMapperModel.objects(res_id=res_id).first()
            new_record = None
            if existing_record is None:
                new_record = ResMapperModel(
                    res_id=res_id,
                    res_doc_id=res_doc_id,
                    res_idx_id=res_idx_id,
                    is_dup=is_dup
                )
            if new_record:
                new_record.save()
                return True
            return False
        except (SaveConditionError, ValidationError):
            return False
