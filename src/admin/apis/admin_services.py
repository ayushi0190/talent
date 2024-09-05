
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT

from src.admin.config.admin_configs import common_adm_settings
from src.admin.helpers.admin_helpers import filter_config_data, send_mail_simplify_hire
from src.admin.interfaces.admin_interface import AdminInterface
from src.db.crud.admin.auth_schema import AuthSchema
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.helpers.misc_helpers import generate_resume_bucket, generate_job_bucket
from src.utilities.token import JWTToken
from src.utilities.tasks import send_clt_reg_taltpool


class AdminServices(AdminInterface):
    """
    Admin services
    """

    def register_client(self, request, data: dict) -> dict:
        """
        Get the result from Job Board
        :param request: Request
        :param data: Dictionary
        :return:
        """
        result = {}
        user_info = {}
        update_job_res_idx_info = {}
        active_model = CltRegSchema()
        auth_user = AuthSchema()
        filtered_data = filter_config_data(data)
        if data.requested_for == "Create":
            if active_model.add(request, filtered_data):
                result_data = active_model.get_client_info(request, filtered_data.get("clt_id"))
                client_resume_index_id = generate_resume_bucket(request, result_data.clt_id)
                client_job_index_id = generate_job_bucket(request, result_data.clt_id)
                if client_job_index_id and client_job_index_id:
                    update_job_res_idx_info.update({
                        "clt_id": result_data.clt_id,
                        "clt_res_idx_id": client_resume_index_id
                    })
                if len(update_job_res_idx_info) > 0 and \
                    active_model.update_client_resume_and_job_index(request, update_job_res_idx_info):
                    # Generate token here
                    jwt = JWTToken()
                    token = jwt.generate_token({'clt_id': result_data.clt_id})
                    user_info.update({
                        "name": result_data.clt_name,
                        "clt_id": result_data.clt_id,
                        "auth_type": common_adm_settings.get("CLIENT_AUTH_TYPE"),
                        "token": token
                    })
                    if auth_user.add(user_info):
                        send_clt_reg_taltpool.delay(result_data.clt_name, result_data.clt_id)
                        score = []
                        if result_data.srv_sco:
                            if result_data.tol_sov:
                                score.append("sovren")
                            if result_data.tol_ope:
                                score.append("opening")
                            if result_data.tol_sim:
                                score.append("simplifyai")
                            request.app.logger.info("Score during registration %s" % score)
                        send_mail_simplify_hire(request, result_data.clt_name, result_data.clt_id,
                                                score)
                        result.update({
                            "code": HTTP_200_OK,
                            "message": "Client information added.",
                            "client_id": result_data.clt_id
                        })
                    else:
                        result.update({
                            "code": HTTP_400_BAD_REQUEST,
                            "message": "Unable to add client.",
                            "client_id": None
                        })
                else:
                    result.update({
                        "code": HTTP_204_NO_CONTENT,
                        "message": "All information of the client could not be added.",
                        "client_id": None
                    })
            else:
                result.update({
                    "code": HTTP_400_BAD_REQUEST,
                    "message": "Unable to add client.",
                    "client_id": None
                })
        else:
            updated_client_id = active_model.update_client_info(request, filtered_data)
            if updated_client_id:
                result.update({
                    "code": HTTP_200_OK,
                    "message": "Client information updated.",
                    "client_id": updated_client_id
                })
            else:
                result.update({
                    "code": HTTP_400_BAD_REQUEST,
                    "message": "Unable to update client.",
                    "client_id": None
                })
        return result
