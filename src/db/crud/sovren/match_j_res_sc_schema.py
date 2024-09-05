# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Database related operations for model MatchJResScModel
@author <ankits@simplifyvms.com>
"""
from mongoengine.errors import SaveConditionError, ValidationError

from src.db.config.db import DataManager

from src.db.models.sovren.match_j_res_sc import MatchJResScModel
from src.utilities.custom_logging import cust_logger as logger

DataManager.get_instance()

class MatchJResScSchema:
    """ parse resume """

    def add(self,request, data: dict, parser: str) -> bool:
        """
        Add record
        :param data: Dictionary
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = MatchJResScModel.objects(
                    res_id=data["res_id"], job_id=data["job_id"],
                    pars_typ=parser).first()
            new_record = None

            if existing_record is None:
                new_record = MatchJResScModel(
                    job_idx_id=data.get("job_idx_id"),
                    job_id=data.get("job_id"),
                    res_id=data.get("res_id"),
                    res_idx_id=data.get("res_idx_id"),
                    scr_res=data.get("scr_res"),
                    clt_id=data.get("clt_id"),
                    pars_typ = parser
                )

            if new_record:
                new_record.save()
                logger.info("Saved New record ")
                return True
            return False
        #except (SaveConditionError, ValidationError):
        except Exception as ex:
            logger.error("Error in saving score %s " % str(ex))
            return False


    def get(self, res_id: str, job_id: str) -> dict:
        """
        Get the record by resume_id
        :param res_id:
        :return:
        """
        return MatchJResScModel.objects(res_id=res_id, job_id=job_id).first()

    def get_by_parser(self, res_id: str, job_id: str, clt_id: str, parser: str) -> dict:
        """
        Get the record by resume_id
        :param res_id:
        :return:
        """
        return MatchJResScModel.objects(res_id=res_id, job_id=job_id, 
                                        clt_id=clt_id, pars_typ=parser).first()

    def get_scored_resume(self, res_id: str, job_id: str, clt_id: str, parser: str) -> dict:
        """
        Get the record by resume_id
        :param res_id:
        :param job_id:
        :return:
        """
        return MatchJResScModel.objects(res_id=res_id, job_id=job_id, 
                                        clt_id=clt_id, pars_typ=parser).first()
