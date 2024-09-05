# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Database related operations for model PrsJobInfModel
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime
from src.db.config.db import DataManager
from src.db.models.sovren.prs_job_inf import PrsJobInfModel
from src.utilities.custom_logging import cust_logger as logger

DataManager.get_instance()


class PrsJobInfSchema:
    """Parsed Job Info Schema"""
    def get(self, job_document_id: str) -> dict:
        """
        Get the record by job_id
        :param job_id:
        :return:
        """
        return PrsJobInfModel.objects(job_id=job_document_id).first()

    def get_by_parser(self, job_document_id: str, client_id: str, parser: str) -> dict:
        """
        Get the record by job_id
        :param job_id:
        :return:
        """
        return PrsJobInfModel.objects(job_id=job_document_id, clt_id=client_id,
                                      pars_typ=parser).first()

    def save_job(self, request, index_id: str, job_id: str, resp: str,  
                 clt_id: str, prs_time: int, parser: str) -> bool:
        """
        Add record
        :param job_id: String
        :param index_id: String
        :param job_id: String
        :param resp: String
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = PrsJobInfModel.objects(
                job_id=job_id,clt_id=clt_id, pars_typ=parser).first()
            if existing_record is None:
                new_record = PrsJobInfModel(
                    index_id=index_id,
                    job_id=job_id,
                    job_res=resp,
                    clt_id=clt_id,
                    prs_time=prs_time,
                    pars_typ = parser
                )
                if new_record.save():
                    return True
            return False
        #except (SaveConditionError, ValidationError):
        #    return False
        except Exception as ex:
            logger.error("Error in saving Parse JOB %s " % str(ex))
            return False

    def update_norm_resp(self, job_id: str, clt_id: str, parser: str, norm_resp: str) -> dict:
        """
        Save the normalized job by resume_id and parser_type for client
        :param res_id: String
        :param clt_id: String
        :param parser: String
        :param norm_resp: String
        :return:
        """
        try:
            existing_record = PrsJobInfModel.objects(
                job_id=job_id, clt_id=clt_id, pars_typ=parser).first()
            if existing_record:
                data = {}
                data.update({"norm_resp": norm_resp,
                             "updated_at": datetime.utcnow()
                             })
                if existing_record.update(**data):
                    return True
            return False
        except Exception as ex:
            logger.error("Exception in updating normalized job: '%s'" % str(ex))
            return False

    def get_latest_inserted_record(self) -> dict:
        """
        Get latest inserted record
        :return:
        """
        # Search in prs_jobs_inf model with reverse order sorting on 'created_at'
        return PrsJobInfModel.objects.order_by('-created_at')[0]

    def delete_job(self, job_id: str) -> bool:
        """
        Delete Job record on Job id
        :return:
        """
        # Delete job on the basis of job id
        return PrsJobInfModel.objects(job_id=job_id).delete()

    def check_job_id(self, request, job_id: str, clt_id: str, parser: str) -> dict:
        """
        Check JOB Id based on Client ID
        :param job_id:
        :return:
        """
        try:
            job_obj = PrsJobInfModel.objects(job_id=job_id, clt_id=clt_id, 
                                             pars_typ=parser).first()
            if job_obj:
                return True
            else:
                return False
        except Exception as ex:
            logger.error("Error in check_job_id based  %s " % str(ex))
            return False

    def get_stat_job(self, request, clt_id: str, start_date: str) -> dict:
        """
        Check Parsing Stats based on Client ID and Start Date
        :param clt_id:
        :return:
        """
        try:
            job_obj = PrsJobInfModel.objects(clt_id=clt_id,created_at__gt=start_date)
            if job_obj:
                count = job_obj.count()
                job_ids_list = [job_info.job_id for job_info in job_obj]
                return count,job_ids_list
            else:
                return False
        except Exception as ex:
            logger.error("Error in clt_id based  %s " % str(ex))
            return False
