
from mongoengine.errors import SaveConditionError, ValidationError

from src.db.config.db import DataManager
from src.db.models.common.mat_idx import MatIdxModel
from src.utilities.custom_logging import cust_logger as logger

DataManager.get_instance()


class MatchingIndexSchema:
    """ MatchingIndexSchema """

    def get(self, data: dict) -> bool:
        """
        Get record
        :param data: Dictionary
        :return:
        """
        # Check if searched content already exist or not
        existing_record = MatIdxModel.objects(
            idx_id=data.get("index_id"), idx_tpe=data.get("index_type")
        ).first()
        if existing_record is None:
            return False
        return True

    def check_index(self, data: dict) -> bool:
        """
        Check index id exist or not based on index id and index type
        :param data: Dictionary
        :return:
        """
        try:
            # Check if searched content already exist or not
            existing_record = MatIdxModel.objects(
                idx_id=data.get("index_id"), idx_tpe=data.get("index_type")
            ).first()
            if existing_record is None:
                return False
            return True
        except (SaveConditionError, ValidationError):
            return False
        except Exception as ex:
            logger.error("Error in checking index %s " % str(ex))
            return False

    def create_record(self, request, index_id: str, index_type: str) -> bool:
        """
        Create record
        :param index_type: String
        :param index_id: String
        :return:
        """
        # Check if searched content already exist or not
        try:
            existing_record = MatIdxModel.objects(
                idx_id=index_id, idx_tpe=index_type
            ).first()
            if existing_record is None:
                new_record = MatIdxModel(idx_id=index_id, idx_tpe=index_type)
                if new_record.save():
                    return True
            return False
        except (SaveConditionError, ValidationError):
            return False
        except Exception as ex:
            logger.error("Error in saving score %s " % str(ex))
            return False

    def get_list(self, data: dict) -> bool:
        """
        Get record
        :param data: Dictionary
        :return:
        """
        # Check if searched content already exist or not
        existing_record = MatIdxModel.objects(idx_tpe=data.get("index_type"))
        if existing_record is None:
            return []
        return existing_record

    def delete_index(self, index_id: str):

        """
        Delete job index id record on index id
        :return:
        """
        # Delete job index id on the basis of job index id

        return MatIdxModel.objects(idx_id=index_id).delete()

    def get_index_id_by_bucket_source_name(self, bucket_source: str):

        """
        Get Index_ID By Bucket Source Name
        :return:
        """
        bucket_source = [ele.upper() for ele in bucket_source]
        existing_record = MatIdxModel.objects(idx_tpe="Job")
        bucket_list = []
        for ele in bucket_source:
            job_index_list = [j.idx_id for j in existing_record if ele in j.idx_id.split('-')]
            bucket_list.extend(job_index_list)
        return bucket_list
