
from datetime import datetime
#import pdb #unused

from mongoengine import SaveConditionError, ValidationError

from src.db.config.db import DataManager
from src.db.models.admin.clt_reg import CltRegModel
from src.utilities.custom_logging import cust_logger as logger

DataManager.get_instance()


class CltRegSchema:
    """ CltRegSchema """

    def add(
            self, request, data: dict) -> dict:
        """
        Add record
        :param request:
        :param data: Dictionary
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = CltRegModel.objects(
                clt_id=data.get("clt_id")
            ).first()
            if existing_record is None:
                new_record = CltRegModel(
                    clt_name=data.get("clt_name"),
                    reg_dt=data.get("reg_dt"),
                    clt_id=data.get("clt_id"),
                    cont_prd=data.get("cont_prd"),
                    pol_shr=data.get("pol_shr"),
                    pol_prv=data.get("pol_prv"),
                    srv_prs=data.get("srv_prs"),
                    srv_mth=data.get("srv_mth"),
                    srv_src=data.get("srv_src"),
                    srv_sco=data.get("srv_sco"),
                    prs_job=data.get("prs_job"),
                    prs_res=data.get("prs_res"),
                    sml_job=data.get("sml_job"),
                    dis_can=data.get("dis_can"),
                    sgt_can=data.get("sgt_can"),
                    sgt_job=data.get("sgt_job"),
                    cmp_can=data.get("cmp_can"),
                    get_res=data.get("get_res"),
                    get_job=data.get("get_job"),
                    src_job=data.get("src_job"),
                    sco_res=data.get("sco_res"),
                    tol_sov=data.get("tol_sov"),
                    tol_ope=data.get("tol_ope"),
                    tol_sim=data.get("tol_sim"),
                    set_wgts=data.get("set_wgts")

                )
                if new_record.save():
                    return True
            return False
        except (SaveConditionError, ValidationError) as error:
            logger.error("Exception in adding client '%s'" % error)

    def get_client_info(self, request, clt_id: str) -> dict:
        """
        Get client information
        :param request:
        :param clt_id: String
        :return:
        """
        try:
            return CltRegModel.objects(clt_id=clt_id).first()
        except Exception as es:
            logger.error("Exception in accessing client record '%s'" % es)

    def del_client_info(self, request, clt_id: str) -> bool:
        """
        Delete entry with given clt_id
        :param request:
        :param clt_id: String
        :return:
        """
        try:
            return CltRegModel.objects(clt_id=clt_id).delete()
        except Exception as es:
            logger.error("Exception in deleting client record '%s'" % es)

    def get_client_name_by_id(self, request, clt_id: str) -> str:
        """
        Find client name by id
        :param request:
        :param clt_id:
        :return:
        """
        try:
            response = CltRegModel.objects.filter(clt_id=clt_id).values_list('clt_name')
            return response[0]
        except Exception as es:
            logger.error("Unable to find client '%s'" % es)

    def update_client_info(self, request, data: dict) -> bool or str:
        """
        Update client information
        :param request:
        :param data:
        :return:
        """
        try:
            existing_record = CltRegModel.objects(
                clt_name=data.get("clt_name")
            )
            if existing_record:
                data.update({
                    "clt_id": existing_record[0].clt_id,
                    "updated_at": datetime.utcnow()
                })
                if existing_record.update(**data):
                    return existing_record[0].clt_id
            return False
        except (SaveConditionError, ValidationError) as error:
            logger.error("Exception in updating client '%s'" % error)

    def update_client_resume_and_job_index(self, request, data: dict) -> bool:
        """
        Update client resume and job index
        :param request:
        :param data:
        :return:
        """
        try:
            existing_record = CltRegModel.objects(
                clt_id=data.get("clt_id")
            )
            if existing_record:
                data.update({
                    "updated_at": datetime.utcnow()
                })
                if existing_record.update(**data):
                    return True
            return False
        except (SaveConditionError, ValidationError) as error:
            logger.error("Exception in updating client '%s'" % error)
