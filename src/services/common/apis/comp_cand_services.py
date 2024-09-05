"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Compare Candidates related services
@author <ankits@simplifyvms.com>
"""

from fastapi import status
from pydantic import ValidationError

from src.services.sovren.apis.comp_cand_to_job_services import \
    CompCandToJobServices
from src.services.sovren.interfaces.comp_cand_interface import \
    CompareCandidateInput
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.helpers.misc_helpers import get_authorized_services

class CompCandServices:
    """
    Comp Cand to Job services class
    """

    def call_comp_cand_to_job(self, request, payload: CompareCandidateInput):
        """
        Compare candidates against a JOB on the basis of services requested
        :param payload: CompareCandidateInput
        :return:
        """
        service_info = get_authorized_services(request)
        try:
            # If the client info exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    comp_cand_object = CompCandToJobServices()
                    return comp_cand_object.list_compare_candidates_info_with_sovren(
                        request, payload)
                # If selected tool is Opening
                if service_info.tol_ope:
                    pass
                # If selected tool is Simplifyai
                if service_info.tol_sim:
                    pass
            else:
                return dict({
                    'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                    'message': "No Client Information Exist"
                })

        except ValidationError as exc:
            return dict({
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': exc.errors()
            })
