# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Get Parsed Candidate Resume
@author <sreddy@simplifyvms.com>
"""

from typing import Dict

from src.services.sovren.interfaces.searchers.get_candidate_resume_interface import GetCandidateResumeInterface
from src.db.crud.sovren.mp_tp_res_schema import MpTpResSchema
from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from starlette.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from src.db.crud.sovren.intern_res_schema import InternResSchema
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema

class GetCandidateResumeServices(GetCandidateResumeInterface):
    """
    GetParsed Job services class
    """

    def get_candidate_resume(self, request, resume_id: str) -> Dict:
        """
        Get the detail of matching Job
        :param resume_id:
        :return: Dict
        """
        clt_id = request.headers['client_id']
        audit_model = AuditTrailsSchema()
        service_name = request.url.path
        response = {}
        prs_res_info = PrsResInfSchema()
        intern_info = InternResSchema()
        if not resume_id:
            extracted_data = {
                'code': HTTP_400_BAD_REQUEST,
                'message': 'Unable to perform operation, ' +
                           'no information given',

            }
            request.app.logger.debug(extracted_data)
            return extracted_data
        if resume_id == '':
            response = {
                'code': HTTP_400_BAD_REQUEST,
                'message': 'Unable to perform operation, ' +
                           'resume id not given'

            }
        else:
            prs_resume = prs_res_info.get(resume_id)
            intern_resume = intern_info.get(resume_id)
            if prs_resume:
                result = []
                result.append({
                    'Id': prs_resume.res_id,
                    'Resume': prs_resume.res_b64,
                    'FileExtension': "pdf"
                })
                response.update({
                    'code' : HTTP_200_OK,
                    'data' : result
                })
                audit_model.add(service_name,clt_id)
            elif intern_resume:
                result = []
                result.append({
                    'Id': intern_resume.res_id,
                    'Resume': intern_resume.res_b64,
                    'FileExtension': "pdf"
                })
                response.update({
                    'code' : HTTP_200_OK,
                    'data' : result
                })
                audit_model.add(service_name,clt_id)
            else:
                response.update({
                    'code' : HTTP_204_NO_CONTENT,
                    'message' : 'No Information to retrieve'
                })
        request.app.logger.debug(response)
        return response
