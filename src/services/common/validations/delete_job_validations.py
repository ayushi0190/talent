# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Delete resume validations
@author <satya@simplifyvms.com>
"""

from pydantic import BaseModel, validator


class DeleteJobValidations(BaseModel):
    """
    Delete job validations
    """
    job_id: str
    delete_index: bool

    @validator("job_id")
    def job_id_must_be_str(cls, job_id):
        """
        Custom validation message for job_id
        :param job_id:
        :return:
        """

        if job_id is not None or len(job_id) != 0:
            if not isinstance(job_id, str):
                raise ValueError('Must be of string type')
        return job_id

    @validator("delete_index")
    def delete_index_must_be_bool(cls, delete_index):
        """
        Custom validation message for delete_index
        :param delete_index:
        :return:
        """
        if not isinstance(delete_index, bool):
            raise ValueError("Must be of boolean type")
        return delete_index
