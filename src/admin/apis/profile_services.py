
from pydantic import ValidationError
from starlette import status
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from src.admin.interfaces.profile_interface import ProfileInterface
from src.db.crud.admin.clt_cat_wgt_schema import CltCatWgtSchema, CltCatWgtSchema_Old
from src.services.common.helpers.misc_helpers import get_authorized_services


class ProfileServices(ProfileInterface):
    """
    Profile services
    """

    def client_category_weights(self, request, data: dict) -> dict:
        """
        Set default client category and weights
        :param request: Request
        :param data: Dictionary
        :return:
        """
        active_model = CltCatWgtSchema()
        service_info = get_authorized_services(request)
        client_id = request.headers['client_id']
        try:
            # If client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.set_wgts:
                    
                    if active_model.get_cat_weights(client_id, data):
                        update_data = {
                            "job_category": data.job_category,
                            "cat_weights": data.category_weights
                        }
                        if active_model.update_cat_weights(client_id,
                                                           update_data):
                            return dict({
                                'code': HTTP_200_OK,
                                'message': "Category weights updated successfully"
                            })
                        else:
                            return dict({
                                'code': HTTP_400_BAD_REQUEST,
                                'message': "Unable to update category weights"
                            })
                    else:
                        if active_model.add(client_id, data.job_category,
                                            data.category_weights):
                            return dict({
                                'code': HTTP_200_OK,
                                'message': "Category weights added successfully"
                            })
                        else:
                            return dict({
                                'code': HTTP_400_BAD_REQUEST,
                                'message': "Unable to add category weights"
                            })
                else:
                    return dict({
                        'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                        'message': "Not authorized to set category weights"
                    })
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

class ProfileServices_Old(ProfileInterface):
    """
    Profile services
    """

    def client_category_weights(self, request, data: dict) -> dict:
        """
        Set default client category and weights
        :param request: Request
        :param data: Dictionary
        :return:
        """
        result = {}
        active_model = CltCatWgtSchema_Old()
        service_info = get_authorized_services(request)
        try:
            # If client Info Exist
            if service_info:
                # If selected tool is Sovren
                if service_info.set_wgts:
                    if data.job_category is not None:
                        if active_model.get_client_category_weights(request, data):
                            update_data = {
                                "job_category": data.job_category,
                                "categories": data.categories,
                                "weights": data.weights
                            }
                            if active_model.update_client_category_weights_info(request, update_data):
                                return dict({
                                    'code': HTTP_200_OK,
                                    'message': "Category wise default weights updated successfully"
                                })
                            else:
                                return dict({
                                    'code': HTTP_400_BAD_REQUEST,
                                    'message': "Unable to update category wise default weights"
                                })
                        else:
                            if active_model.add(request, data.job_category, data.categories, data.weights):
                                return dict({
                                    'code': HTTP_200_OK,
                                    'message': "Category wise default weights added successfully"
                                })
                            else:
                                return dict({
                                    'code': HTTP_400_BAD_REQUEST,
                                    'message': "Unable to add category wise default weights"
                                })
        except ValidationError as exc:
            return dict({
                'code': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': exc.errors()
            })
