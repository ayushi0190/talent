
from datetime import datetime
#import pdb

from mongoengine import SaveConditionError, ValidationError

from src.db.config.db import DataManager
from src.db.models.admin.clt_cat_wgt import CltCatWgtModel, CltCatWgtModel_Old
from src.utilities.custom_logging import cust_logger as logger

DataManager.get_instance()


class CltCatWgtSchema:
    """ CltCatWgtSchema """

    def add(
            self, client_id, job_category: str, category_weights: dict) -> dict:
        """
        Add record
        :param client_id: String
        :param job_category: String
        :param category_weights: Dict
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = CltCatWgtModel.objects(
                clt_id=client_id, job_category=job_category
            ).first()
            if existing_record is None:
                new_record = CltCatWgtModel(
                    clt_id=client_id,
                    job_category=job_category,
                    cat_weights=category_weights
                )
                if new_record.save():
                    return True
            return False
        except (SaveConditionError, ValidationError) as error:
            logger.error("Exception in adding weights '%s'" % error)
            return False

    def get_cat_weights(self, client_id, job_category: str) -> dict:
        """
        Get client category weights information
        :param client_id:
        :param data: Dict
        :return:
        """
        try:
            return CltCatWgtModel.objects(
                    clt_id=client_id, job_category=job_category).first()
        except Exception as es:
            logger.error("Exception in accessing client record '%s'" % es)

    def del_cat_weights(self, client_id, job_category: str) -> bool:
        """
        Delete entry with given clt_id
        :param data: Dict
        :param client_id:
        :return:
        """
        try:
            return CltCatWgtModel.objects(
                    clt_id=client_id, job_category=job_category).delete()
        except Exception as es:
            logger.error("Exception in deleting client record '%s'" % es)
            return False

    def update_cat_weights(self, client_id, data: dict) -> bool or str:
        """
        Update client category and weights information
        :param client_id:
        :param data:
        :return:
        """
        try:
            existing_record = CltCatWgtModel.objects(
                clt_id=client_id, job_category=data.get("job_category")
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

class CltCatWgtSchema_Old:
    """ CltCatWgtSchema """

    def add(
            self, request, job_category: str, categories: list, weights: list) -> dict:
        """
        Add record
        :param request:
        :param job_category: String
        :param categories: List
        :param weights: List
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = CltCatWgtModel_Old.objects(
                clt_id=request.headers['client_id'],
                job_category=job_category
            ).first()
            if existing_record is None:
                new_record = CltCatWgtModel_Old(
                    clt_id=request.headers['client_id'],
                    job_category=job_category,
                    categories=categories,
                    weights=weights
                )
                if new_record.save():
                    return True
            return False
        except (SaveConditionError, ValidationError) as error:
            logger.error("Exception in adding weights '%s'" % error.message)

    def get_client_category_weights(self, request, data: dict) -> dict:
        """
        Get client category weights information
        :param request:
        :param data: Dict
        :return:
        """
        try:
            return CltCatWgtModel_Old.objects(clt_id=request.headers['client_id'],
                                          job_category=data.job_category).first()
        except Exception as es:
            logger.error("Exception in accessing client record '%s'" % es.message)

    def del_client_category_weights_info(self, request, data: dict) -> bool:
        """
        Delete entry with given clt_id
        :param data: Dict
        :param request:
        :return:
        """
        try:
            return CltCatWgtModel_Old.objects(clt_id=request.headers['client_id'],
                                          job_category=data.job_category).delete()
        except Exception as es:
            logger.error("Exception in deleting client record '%s'" % es.message)

    def update_client_category_weights_info(self, request, data: dict) -> bool or str:
        """
        Update client category and weights information
        :param request:
        :param data:
        :return:
        """
        try:
            existing_record = CltCatWgtModel_Old.objects(
                clt_id=request.headers["client_id"],
                job_category=data.get("job_category")
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
            logger.error("Exception in updating client '%s'" % error.message)
