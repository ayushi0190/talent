# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Database related operations for model MpTpResModel
@author <rchakraborty@simplifyvms.com>
"""
from mongoengine.errors import SaveConditionError, ValidationError
from src.db.config.db import DataManager
from src.db.models.sovren.mp_tp_res import MpTpResModel

DataManager.get_instance()


class MpTpResSchema:
    """MappedTalentPoolResume Schema"""

    def add(self, res_idx_id: str, doc_id: str, res: str, res_b64: str, clt_id: str) -> bool:
        """
        Add record
        :param resp: String
        :param job_ref_num: String
        :param res_id: String
        :param doc_id: String
        :param idx_id: String
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = MpTpResModel.objects(doc_id=doc_id).first()
            if existing_record is None:
                new_record = MpTpResModel(
                    res_idx_id=res_idx_id,
                    res=res,
                    res_b64=res_b64,
                    doc_id=doc_id,
                    clt_id=clt_id
                )
                if new_record.save():
                    return True
                return False
        except (SaveConditionError, ValidationError):
            return False

    def get(self, resume_id: str) -> dict:
        """
        Get the record by resume_id
        :param res_id:
        :return:
        """
        return MpTpResModel.objects(doc_id=resume_id).first()

    def get_data(resume_id: str) -> dict:
        """
        Get the record by resume_id
        :param res_id:
        :return:
        """
        return MpTpResModel.objects(doc_id=resume_id).first()

    def get_candidate_data(document_id: str):
        """
        Get jobs by job_ref_num
        :param job_ref_num: String
        :return:
        """
        return MpTpResModel.objects(document_id=document_id).first()
