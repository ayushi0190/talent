# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Delete resume validations
@author <rchakraborty@simplifyvms.com>
"""

from pydantic import BaseModel, validator


class DeleteResumeValidations(BaseModel):
    """
    Delete resume validations
    """
    resume_id: str
    delete_index: bool

    @validator("resume_id")
    def resume_id_must_be_str(cls, resume_id):
        """
        Custom validation message for resume_id
        :param resume_id:
        :return:
        """

        if resume_id is not None or len(resume_id) != 0:
            if not isinstance(resume_id, str):
                raise ValueError('Must be of string type')
        return resume_id

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
