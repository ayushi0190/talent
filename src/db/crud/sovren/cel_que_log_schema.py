
from typing import Any, Dict, Optional, Tuple, Union
from datetime import datetime

from mongoengine.errors import SaveConditionError, ValidationError

from src.db.config.db import DataManager
from src.db.models.sovren.cel_que_log import CeleryQueLogModel
from src.utilities.custom_logging import cust_logger as logger

DataManager.get_instance()


class CeleryQueLogSchema:
    """ SovQueLogSchema """

    def add_task(self, request):
        """

        """

        # Check if searched content already exist or not
        try:
            existing_record = CeleryQueLogModel.objects(
                job_id=request['job_id'], res_id=request['res_id'],
                req_type = request['req_type'], pars_typ = request.get('parser')
            ).first()
            if existing_record is None:
                new_record = CeleryQueLogModel(
                    res_id = request['res_id'],
                    job_id = request['job_id'],
                    is_pros = request['is_pros'],
                    clt_resp = request['clt_resp'],
                    req_type = request['req_type'],
                    pars_typ = request.get('parser')
                )
                if new_record.save():
                    return True
            return existing_record
        except (SaveConditionError, ValidationError) as ex:
            logger.error("Error in saving Celery queue log: %s" % str(ex))
            return False

    def processdatatodb(self, request):
        """
        Process data to db
        :param request:
        :return:
        """
        object_model = CeleryQueLogModel.objects.filter(
            id=request['pk_id']
        )
        request = {'is_processed': request['flag'],
                   'client_response': request['client_response']}
        object_model.update(**request)
        return object_model[0].id


    def update(self, request):
        """
        Process data to db
        :param request:
        :return:
        """
        try:
            object_model = CeleryQueLogModel.objects.filter(
                res_id=request['res_id'], job_id=request['job_id'],
                req_type = request['req_type'], pars_typ = request.get('parser')
            )
            request = {'is_pros': request['is_pros'],
                       'clt_resp': request['clt_resp'],
                       'updated_at': datetime.utcnow()}
            object_model.update(**request)
            return object_model[0].id
        except Exception as ex:
            logger.error("Error in updating Celery queue log: %s" % str(ex))
            raise ex

