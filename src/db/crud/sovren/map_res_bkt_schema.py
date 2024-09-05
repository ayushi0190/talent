# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Database related operations for model MapResBktModel
@author <rchakraborty@simplifyvms.com>
"""
from mongoengine.errors import SaveConditionError, ValidationError

from src.db.config.db import DataManager

from src.db.models.sovren.map_res_bkt import MapResBktModel

DataManager.get_instance()


class MapResBktSchema:
    """ parse resume """

    def add(self, res_doc_id: str, prs_res: str,
            scr_gen: bool, clt_id: str) -> bool:
        """
        Add record
        :param scr_gen: Boolean
        :param prs_res: String
        :param res_doc_id: String
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = MapResBktModel.objects(res_doc_id=res_doc_id).first()
            if existing_record is None:
                new_record = MapResBktModel(
                    res_doc_id=res_doc_id,
                    prs_res=prs_res,
                    scr_gen=scr_gen,
                    clt_id=clt_id
                )
            if new_record.save():
                return True
            return False
        except (SaveConditionError, ValidationError):
            return False

    def get(self, res_doc_id: str) -> dict:
        """
        Get the record by resume_id
        :param res_doc_id: String
        :return:
        """
        return MapResBktModel.objects(res_doc_id=res_doc_id).first()
