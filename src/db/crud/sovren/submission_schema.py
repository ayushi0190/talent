# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Database related operations for model SubmissionModel
@author <ankits@simplifyvms.com>
"""

from mongoengine.errors import SaveConditionError, ValidationError
from src.db.config.db import DataManager

from src.db.models.sovren.submission_info import SubmissionInfModel
from src.utilities.custom_logging import cust_logger as logger

DataManager.get_instance()


class SubmissionSchema:
    """ submission schema """

    def add_submission(self, request, idx_id: str, res_doc_id: str, res_id: str, job_id: str,
            clt_id: str, name: str, first_name:str, last_name:str, email: str,
            phone: str, vendor: str, response_id: str,questions: str,
            score_required: str, api_source: str, parser: str) -> bool:

        """
        Add record
        :param resp: String
        :param res_id: String
        :param res_doc_id: String
        :param idx_id: String
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = SubmissionInfModel.objects(
                    res_id=res_id, job_id=job_id, pars_typ=parser).first()
            new_record = None
            if existing_record is None:
                new_record = SubmissionInfModel(
                    idx_id=idx_id,
                    res_doc_id=res_doc_id,
                    res_id=res_id,
                    job_id=job_id,
                    clt_id=clt_id,
                    name=name,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone=phone,
                    vendor=vendor,
                    response_id=response_id,
                    questions=questions,
                    score_required=score_required,
                    api_source=api_source,
                    pars_typ=parser
                )
            if new_record:
                if new_record.save():
                    return True
                return False
            return False
        # except (SaveConditionError, ValidationError):
        except Exception as ex:
            logger.error("Error in saving Submission %s " % str(ex))
            return False