# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Database related operations for model JaobParser
@author <rchakraborty@simplifyvms.com>
"""
from mongoengine.errors import SaveConditionError, ValidationError

from src.db.config.db import DataManager
from src.db.models.sovren.prs_job_inf import PrsJobInfModel
from src.utilities.custom_logging import cust_logger as logger

DataManager.get_instance()


class ParsedJobSchema:
    """ JobsToJobSchema """

    def add(
        self,
        index_id: str,
        _index_type: str,
        references: dict,
        job_id: str,
        sovren_response: str,
        clt_id: str
    ) -> bool:
        """
        Add record
        :param sovren_response: String
        :param job_id: String
        :param references: Dictionary
        :param _index_type: String
        :param index_id: String
        :param job_id: String
        :param sovren_response: String
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = PrsJobInfModel.objects(
                job_id=job_id
            ).first()
            if existing_record is None:
                new_record = PrsJobInfModel(
                    index_id=index_id,
                    job_id=job_id,
                    sor_sys=references["sor_sys"],
                    sor_tp=references["sor_tp"],
                    sor_prod=references["sor_prod"],
                    clt_job_id=references["clt_job_id"],
                    job_brd_id=references["job_brd_id"],
                    job_res=sovren_response,
                    clt_id=clt_id
                )
                if new_record.save():
                    return True
            return False
        except (SaveConditionError, ValidationError):
            return False

    def save_job(self, request, index_id: str, job_id: str, sovren_response: str,  
                 clt_id: str, parser: str, prs_time: int) -> bool:
        """
        Add record
        :param sovren_response: String
        :param job_id: String
        :param index_id: String
        :param job_id: String
        :param sovren_response: String
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = PrsJobInfModel.objects(
                job_id=job_id,clt_id=clt_id, pars_typ=parser
            ).first()
            if existing_record is None:
                new_record = PrsJobInfModel(
                    index_id=index_id,
                    job_id=job_id,
                    job_res=sovren_response,
                    clt_id=clt_id,
                    prs_time=prs_time,
                    pars_typ=parser
                )
                if new_record.save():
                    return True
            return False
        #except (SaveConditionError, ValidationError):
        #    return False
        except Exception as ex:
            logger.error("Error in saving Parse JOB %s " % str(ex))
            return False

    def get_job_info(self, request, job_id: str, client_id: str, parser: str) -> dict:
        """
        Get the record by job_id
        :param : res_id
        :param : job_id
        :return:
        """
        try:
            job_obj = PrsJobInfModel.objects(job_id=job_id, clt_id=client_id,
                                             pars_typ=parser).first()
            return job_obj
        except Exception as ex:
            logger.error("Error in get_job_info based on job_id %s " % str(ex))

