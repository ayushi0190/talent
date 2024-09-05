# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Resume mapper helpers
@author <rchakraborty@simplifyvms.com>
"""
from src.db.crud.sovren.res_mapper_schema import ResMapperSchema
from src.services.common.apis.matching_index_services import MatchingIndexServices
from starlette.status import HTTP_304_NOT_MODIFIED


def resume_mapper(parsed_resume: dict, resume_document_id: str, index_id: str, resume_id: str):
    """
    Map resume
    :param parsed_resume:
    :param resume_document_id:
    :param index_id:
    :param resume_id:
    :return:
    """
    extracted_data = {}
    res_mapper = ResMapperSchema()
    index_matcher = MatchingIndexServices()
    #if parsed_resume.get("res_doc_id") == resume_document_id:
    if parsed_resume.res_doc_id == resume_document_id:
        res_bkt = res_mapper.get(resume_document_id, index_id)
        if not res_bkt:
            index_create = index_matcher.create_index(index_id, "Resume")
            if index_create.get('code') == 'Success':
                res_mapper.add(index_id, resume_document_id, resume_id)
        else:

            res_mapper.update(resume_document_id, index_id, resume_id, True)
        extracted_data.update({
            "code": HTTP_304_NOT_MODIFIED,
            "message": "Duplicate Resume"
        })
        return extracted_data
