# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0Graph services
@author <ankits@simplifyvms.com>
"""
from typing import Dict
from pydantic import ValidationError
from starlette.status import HTTP_200_OK,HTTP_422_UNPROCESSABLE_ENTITY

from src.services.common.helpers.misc_helpers import get_authorized_services
from src.services.sovren.apis.graph_services import SovrenGraph


class GraphServices:
    """
    Graph services class
    """

    def call_get_graph(self, request, id:str, source: str) -> Dict:
        """
        It will call Get Graph based on the tool selected by client
        :param : request
        :param : data
        :param : background_task
        :return: JSON output
        """
        #service_info = get_authorized_services(request)

        try:
            # If client Info Exist
            #if service_info:
                # If selected tool is Sovren
                #if service_info.tol_sov:
            if source.lower() == "sovren":

                sovren_graph = SovrenGraph()
                print("In common graph :", id)
                result = sovren_graph.get_graph(request, id)

                return result
            # If selected tool is Opening
            #if service_info.tol_ope:
            #    pass
            # If selected tool is Simplifyai
            #if service_info.tol_sim:
            #    pass
            #else:
            #    return dict({
            #        'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
            #        'message': "No Client Information Exist"
            #    })

        except ValidationError as exc:
            return dict({
                'code': HTTP_422_UNPROCESSABLE_ENTITY,
                'message': exc.errors()
            })
