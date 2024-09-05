"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Parsing Stats Services
@author <rchakraborty@simplifyvms.com>
@author <sreddy@simplifyvms.com>
"""
from typing import List

from fastapi import status
from pydantic import ValidationError

from src.services.common.helpers.misc_helpers import find_words_exists
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.helpers.misc_helpers import get_authorized_services
from src.services.sovren.apis.parsing_stats_services import StatsParsingServices
from src.services.common.validations.parsing_stats_validations import ParsingStatsValidations,AuditStatsValidations
from src.services.sovren.apis.audit_stats_services import StatsAuditServices

class ParsingStatsServices:
    """
    Matcher services class
    """

    def call_parsing_stats(
        self, request, data: ParsingStatsValidations
    ) -> List:
        """
        Get parsing stats on the basis of services requested
        :param request: Request
        :param data:
        :return:
        """
        service_info = get_authorized_services(request)
        try:
            # If the client info exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    stats_prasing = StatsParsingServices()
                    return stats_prasing.get_stat_parsing(request, data.dict())
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

class AuditStatsServices:
    """
    Audit Stats class
    """

    def call_audit_stats(
        self, request, data: AuditStatsValidations
    ) -> List:
        """
        Get parsing stats on the basis of services requested
        :param request: Request
        :param data:
        :return:
        """
        service_info = get_authorized_services(request)
        try:
            # If the client info exist
            if service_info:
                # If selected tool is Sovren
                if service_info.tol_sov:
                    stats_audit = StatsAuditServices()
                    return stats_audit.get_stat_audit(request, data.dict())
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
