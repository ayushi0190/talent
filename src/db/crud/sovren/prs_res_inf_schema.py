# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Database related operations for model PrsResInfModel
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime
from mongoengine.errors import SaveConditionError, ValidationError

from src.db.config.db import DataManager

from src.db.models.sovren.prs_res_inf import PrsResInfModel
from src.db.models.sovren.intern_res import InternResModel
from src.utilities.custom_logging import cust_logger as logger

DataManager.get_instance()


class PrsResInfSchema:
    """ parse resume """

    def add(self, request, idx_id: str, res_doc_id: str, res_id: str,
            resp: str, clt_id: str, doc_md5: str, res_b64: str, prs_time: int,
            pars_typ: str, orig_doc_md5: str, additional_skills: list) -> bool:
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
            existing_record = PrsResInfModel.objects(res_id=res_id, pars_typ=pars_typ).first()
            new_record = None
            if existing_record is None:
                new_record = PrsResInfModel(
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
        # except (SaveConditionError, ValidationError):
        except Exception as ex:
            logger.error("Error in saving Parse Resume %s " % str(ex))
            return False

    def update_norm_resp(self, res_id: str, clt_id: str, parser: str, norm_resp: str) -> dict:
        """
        Save the normalized resume by resume_id and parser_type for client
        :param res_id: String
        :param clt_id: String
        :param parser: String
        :param norm_resp: String
        :return:
        """
        try:
            existing_record = PrsResInfModel.objects(
                res_id=res_id, clt_id=clt_id, pars_typ=parser).first()
            if existing_record:
                data = {}
                data.update({"norm_resp": norm_resp,
                             "updated_at": datetime.utcnow()
                             })
                if existing_record.update(**data):
                    return True
            return False
        except Exception as ex:
            logger.error("Exception in updating normalized resume: '%s'" % str(ex))
            return False

    def get(self, res_id: str) -> dict:
        """
        Get the record by resume_id
        :param res_id:
        :return:
        """
        res_id = res_id.upper()
        return PrsResInfModel.objects(res_id=res_id).first()

    def get_by_parser(self, res_id: str, clt_id: str, parser: str) -> dict:
        """
        Get the record by resume_id and parser_type for client
        :param res_id: String
        :param clt_id: String
        :param parser: String
        :return:
        """
        res_id = res_id.upper()
        res_obj = PrsResInfModel.objects(res_id=res_id, clt_id=clt_id, pars_typ=parser).first()
        if res_obj is None:
            res_obj = InternResModel.objects(res_id=res_id, clt_id=clt_id, pars_typ=parser).first()
        return res_obj

    def get_by_hash_and_skills(self, orig_doc_md5: str, clt_id: str,
                               additional_skills: list) -> dict:
        """
        Get the record by orig_doc_md5, additional skills and client for client
        :return:
        """
        if additional_skills:
            additional_skills.sort()
        res_obj = PrsResInfModel.objects(orig_doc_md5=orig_doc_md5, clt_id=clt_id,
                                additional_skills=additional_skills).first()
        if res_obj is None:
            res_obj = InternResModel.objects(orig_doc_md5=orig_doc_md5, clt_id=clt_id,
                                additional_skills=additional_skills).first()
        if res_obj is None:
            res_obj = PrsResInfModel.objects(orig_doc_md5=orig_doc_md5,
                                additional_skills=additional_skills).first()
        if res_obj is None:
            res_obj = InternResModel.objects(orig_doc_md5=orig_doc_md5,
                                additional_skills=additional_skills).first()
        return res_obj

    def get_by_client(self, doc_md5: str, clt_id: str) -> dict:
        """
        Get the record by doc_md5 and client for client
        :return:
        """
        res_obj = PrsResInfModel.objects(doc_md5=doc_md5, clt_id=clt_id).first()
        if res_obj is None:
            res_obj = InternResModel.objects(doc_md5=doc_md5, clt_id=clt_id).first()
        if res_obj is None:
            res_obj = PrsResInfModel.objects(doc_md5=doc_md5).first()
        if res_obj is None:
            res_obj = InternResModel.objects(doc_md5=doc_md5).first()
        return res_obj

    def get_graph_data(self,request, res_id: str, parser: str='sovren') -> dict:
        """
        Get the record by resume_id
        :param res_id: 
        :param request:
        :return:
        """
        res_id = res_id.upper()
        try:
            res_obj = PrsResInfModel.objects(res_id=res_id, pars_typ=parser).first()
            if res_obj is None:
                res_obj = InternResModel.objects(res_id=res_id, pars_typ=parser).first()
            return res_obj

        except Exception as ex:
            logger.error("Error in get_graph_data based on res_id %s " % str(ex))
            return None

    def get_resume_info(self, request, doc_md5: str, clt_id: str, parser: str) -> dict:
        """
        Get the record by resume_id
        :param res_id:
        :return:
        """
        try:
            res_obj = PrsResInfModel.objects(doc_md5=doc_md5, clt_id=clt_id, pars_typ=parser).first()
            if res_obj is None:
                res_obj = PrsResInfModel.objects(doc_md5=doc_md5, pars_typ=parser).first()

                # Add a logic for Shared Pool, to check if resume exist in Shared Pool
                if res_obj is None:
                    res_obj = InternResModel.objects(doc_md5=doc_md5, pars_typ=parser).first()

            return res_obj
        except Exception as ex:
            logger.error("Error in get_resume_info based on md5_hash %s " % str(ex))
            return None

    def check_resume_id(self, request, res_id: str, clt_id: str, parser: str) -> dict:
        """
        Check resume Id based on Client ID
        :param res_id:
        :return:
        """
        res_id = res_id.upper()
        try:
            res_obj = PrsResInfModel.objects(res_id=res_id, clt_id=clt_id, pars_typ=parser).first()
            if res_obj:
                return True
            else:
                res_obj = InternResModel.objects(res_id=res_id, clt_id=clt_id, pars_typ=parser).first()
                if res_obj:
                    return True
                else:
                    return False
        except Exception as ex:
            logger.error("Error in get_resume_info based on md5_hash %s " % str(ex))
            return False

    def get_data(res_id: str, parser: str=None) -> dict:
        """
        Get the record by resume_id
        :param res_id:
        :return:
        """
        res_id = res_id.upper()
        if parser:
            return PrsResInfModel.objects(res_id=res_id, pars_typ=parser).first()
        else:
            return PrsResInfModel.objects(res_id=res_id).first()


    def get_latest_inserted_record() -> dict:
        """
        Get latest inserted record
        :return:
        """
        # Search in prs_res_inf model with reverse order sorting on 'created_at'
        return PrsResInfModel.objects.order_by('-created_at')[0]

    def delete_resume(self, res_id: str) -> bool:
        """
        Delete resume record on resume id
        :return:
        """
        # Delete resume on the basis of resume id
        res_id = res_id.upper()
        return PrsResInfModel.objects(res_id=res_id).delete()

    def get_stat_resumes(self, request, clt_id: str, start_date: str) -> dict:
        """
        Check Parsing Stats for Resumes based on Client ID and Start Date
        :param clt_id:
        :return:
        """
        try:
            res_obj = PrsResInfModel.objects(clt_id=clt_id,created_at__gt=start_date)
            if res_obj:
                count = res_obj.count()
                res_ids_list = [res_info.res_id for res_info in res_obj]
                return count,res_ids_list
            else:
                return False
        except Exception as ex:
            logger.error("Error in clt_id based  %s " % str(ex))
            return False
