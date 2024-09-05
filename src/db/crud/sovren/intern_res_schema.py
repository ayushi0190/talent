# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Database related operations for model InternResModel
@author <ankits@simplifyvms.com>
"""
from mongoengine.errors import SaveConditionError, ValidationError

from src.db.config.db import DataManager

from src.db.models.sovren.intern_res import InternResModel

DataManager.get_instance()


class InternResSchema:
    """ parse resume """

    def add(self, request, idx_id: str, res_doc_id: str, res_id: str,
            resp: str, clt_id: str, doc_md5: str, res_b64: str, 
            prs_time: int, pars_typ: str, orig_doc_md5: str,
            additional_skills: list) -> bool:
        """
        Add record
        :param resp: String
        :param res_id: String
        :param res_doc_id: String
        :param idx_id: String
        :return:
        """
        if additional_skills:
            additional_skills.sort()
        # Check if searched content already exist or not
        try:
            existing_record = InternResModel.objects(res_id=res_id, pars_typ=pars_typ).first()
            new_record = None
            if existing_record is None:
                new_record = InternResModel(
                    idx_id=idx_id,
                    res_id=res_id,
                    res_doc_id=res_doc_id,
                    doc_md5=doc_md5,
                    resp=resp,
                    clt_id=clt_id,
                    res_b64=res_b64,
                    prs_time=prs_time,
                    orig_doc_md5=orig_doc_md5,
                    additional_skills=additional_skills,
                    pars_typ=pars_typ
                )
            if new_record:
                if new_record.save():
                    return True
                return False
            return False
        except Exception as ex:
            request.app.logger.error("Error in saving Parse Resume under Internal Bucket %s " % str(ex))
            return False

    def get(self, res_id: str) -> dict:
        """
        Get the record by resume_id
        :param res_id:
        :return:
        """
        res_id = res_id.upper()
        return InternResModel.objects(res_id=res_id).first()

    def get_by_parser(self, res_id: str, clt_id: str, parser: str) -> dict:
        """
        Get the record by resume_id
        :param res_id:
        :return:
        """
        res_id = res_id.upper()
        return InternResModel.objects(res_id=res_id, clt_id=clt_id, pars_typ=parser).first()
