# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Database related operations for model CntTpModel
@author <rchakraborty@simplifyvms.com>
"""
from src.db.config.db import DataManager
from src.db.models.sovren.cnt_tp import CntTpModel

DataManager.get_instance()


class CntFrmTpSchema:
    """
    Contact from talent pool schema
    """

    def get(self, resume_id: str) -> dict:
        """
        Get record
        :param resume_id:
        :return:
        """
        return CntTpModel.objects(res_id=resume_id).first()
