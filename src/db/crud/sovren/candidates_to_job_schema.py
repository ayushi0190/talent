
from typing import Any, Dict, Optional, Tuple, Union

from mongoengine.errors import SaveConditionError, ValidationError

from src.db.config.db import DataManager
from src.db.models.sovren.cand_to_job import CandToJobModel

DataManager.get_instance()


class CandidatesToJobSchema:
    """ CandidatesToJobSchema """

    def add(
        self, job_id: str, result_response: dict, clt_id: str
    ) -> Union[Union[bool, None, Tuple[Dict[str, Optional[str]], int]], Any]:
        """
        Add record
        :param job_refrence_number: String
        :param result_response: Dictionary
        param clt_id: String
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = CandToJobModel.objects(
                job_id=job_id
            ).first()
            if existing_record is None:
                new_record = CandToJobModel(
                    job_id=job_id, srch_res=result_response, clt_id=clt_id
                )
                if new_record.save():
                    return True
            return existing_record
        except (SaveConditionError, ValidationError):
            return False

    def get_jobs(self, job_id: str,clt_id: str) -> dict:
        """
        Get jobs by job_ref_num
        :param job_ref_num: String
        :return:
        """
        return CandToJobModel.objects(job_id=job_id, clt_id=clt_id).first()

    def del_jobs(self, job_id: str, clt_id: str) -> bool:
        """
        Delete entry with given job_ref_num
        :param job_ref_num: String
        :return:
        """
        return CandToJobModel.objects(job_id=job_id, clt_id=clt_id).delete()

    def add_searched_result(self, job_id: str, src_res: list, clt_id: str) -> bool:
        """
        Add searched result
        :param job_ref_num: String
        :param mth_jobs: List
        :param src_res: List
        :return: Bool
        """
        try:
            existing_record = CandToJobModel.objects(
                job_id=job_id).first()
            if not existing_record:
                new_record = CandToJobModel(
                    job_id=job_id, srch_res=src_res, clt_id=clt_id)
                if new_record.save():
                    return True
            return False
        except (SaveConditionError, ValidationError):
            return False

    @staticmethod
    def get_candidates_search_result(job_id: str) -> dict:
        """
        Get jobs by job_id
        :param job_id: String
        :return:
        """
        return CandToJobModel.objects(job_id=job_id).first()