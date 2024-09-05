# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Database related operations for model ResumesToResume
@author <rchakraborty@simplifyvms.com>
@author <sreddy@simplifyvms.com>
"""
from typing import Any, Dict, Optional, Tuple, Union

from mongoengine.errors import SaveConditionError, ValidationError

from src.db.config.db import DataManager
from src.db.models.sovren.resms_to_resm import ResumesToResume

DataManager.get_instance()


class ResumesToResumeSchema:
    """ ResumesToResumeSchema """

    def add(
        self, res_id: str, result_response: dict, clt_id: str
    ) -> Union[Union[bool, None, Tuple[Dict[str, Optional[str]], int]], Any]:
        """
        Add record
        :param job_refrence_number: String
        :param result_response: Dictionary
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = ResumesToResume.objects(
                res_id=res_id
            ).first()
            if existing_record is None:
                new_record = ResumesToResume(
                    res_id=res_id, srch_res=result_response,
                    clt_id=clt_id
                )
                if new_record.save():
                    return True
            return existing_record
        except (SaveConditionError, ValidationError):
            return False

    def get_resumes(self, res_id: str, clt_id: str) -> dict:
        """
        Get jobs by res_id
        :param res_id: String
        :return:
        """
        return ResumesToResume.objects(res_id=res_id, clt_id=clt_id).first()

    def del_jobs(self, res_id: str, clt_id:str) -> bool:
        """
        Delete entry with given job_ref_num
        :param job_ref_num: String
        :return:
        """
        return ResumesToResume.objects(res_id=res_id, clt_id=clt_id).delete()

    def add_searched_result(self, res_id: str, src_res: list, clt_id: str) -> bool:
        """
        Add searched result
        :param job_ref_num: String
        :param mth_jobs: List
        :param src_res: List
        :return: Bool
        """
        try:
            existing_record = ResumesToResume.objects(
                res_id=res_id).first()
            if not existing_record:
                new_record = ResumesToResume(
                    res_id=res_id, srch_res=src_res, clt_id=clt_id)
                if new_record.save():
                    return True
            return False
        except (SaveConditionError, ValidationError):
            return False
