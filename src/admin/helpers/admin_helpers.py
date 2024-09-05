

import json
import uuid
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.helpers.misc_helpers import remove_special_characters, filter_xss
from src.admin.config.admin_configs import common_adm_settings
from src.services.common.config import common_config
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_202_ACCEPTED
from src.config import config
import emails


def filter_config_data(data: dict) -> dict:
    """
    Filter configuration data
    :param data:
    :return:
    """
    company_name = filter_xss(data.company_name, True)
    if data.requested_for == "Create":
        clt_id = str(uuid.uuid4())
        return {
            "clt_name": company_name,
            "reg_dt": data.registration_date,
            "clt_id": clt_id,
            "cont_prd": data.contract_period,
            "pol_shr": data.pol_shr,
            "pol_prv": data.pol_prv,
            "srv_prs": data.services_to_use.parsing,
            "srv_mth": data.services_to_use.matching,
            "srv_src": data.services_to_use.searching,
            "srv_sco": data.services_to_use.scoring,
            "prs_job": data.services_to_use.parser_service_to_use.parse_job,
            "prs_res": data.services_to_use.parser_service_to_use.parse_resume,
            "sml_job": data.services_to_use.matcher_service_to_use.similar_jobs,
            "dis_can": data.services_to_use.matcher_service_to_use.discover_candidates,
            "sgt_can": data.services_to_use.matcher_service_to_use.suggested_candidates,
            "sgt_job": data.services_to_use.matcher_service_to_use.suggested_jobs,
            "cmp_can": data.services_to_use.matcher_service_to_use.compare_candidates,
            "get_res": data.services_to_use.searcher_services_to_use.get_parsed_resume,
            "get_job": data.services_to_use.searcher_services_to_use.get_parsed_job,
            "src_job": data.services_to_use.searcher_services_to_use.search_jobs,
            "sco_res": data.services_to_use.scorer_services_to_use.score_resume_job,
            "tol_sov": data.tool_to_use.sovren,
            "tol_ope": data.tool_to_use.opening,
            "tol_sim": data.tool_to_use.simpai,
            "set_wgts": data.set_wgts
        }
    else:
        return {
            "clt_name": company_name,
            "reg_dt": data.registration_date,
            "cont_prd": data.contract_period,
            "pol_shr": data.pol_shr,
            "pol_prv": data.pol_prv,
            "srv_prs": data.services_to_use.parsing,
            "srv_mth": data.services_to_use.matching,
            "srv_src": data.services_to_use.searching,
            "srv_sco": data.services_to_use.scoring,
            "prs_job": data.services_to_use.parser_service_to_use.parse_job,
            "prs_res": data.services_to_use.parser_service_to_use.parse_resume,
            "sml_job": data.services_to_use.matcher_service_to_use.similar_jobs,
            "dis_can": data.services_to_use.matcher_service_to_use.discover_candidates,
            "sgt_can": data.services_to_use.matcher_service_to_use.suggested_candidates,
            "sgt_job": data.services_to_use.matcher_service_to_use.suggested_jobs,
            "cmp_can": data.services_to_use.matcher_service_to_use.compare_candidates,
            "get_res": data.services_to_use.searcher_services_to_use.get_parsed_resume,
            "get_job": data.services_to_use.searcher_services_to_use.get_parsed_job,
            "src_job": data.services_to_use.searcher_services_to_use.search_jobs,
            "sco_res": data.services_to_use.scorer_services_to_use.score_resume_job,
            "tol_sov": data.tool_to_use.sovren,
            "tol_ope": data.tool_to_use.opening,
            "tol_sim": data.tool_to_use.simpai,
            "set_wgts": data.set_wgts
        }


def find_field_name(service_name: str) -> str:
    """
    Find Relevant Service Name
    """
    endpoints = {
        '/parse/job/by/id': 'prs_job',
        '/parse/job/by/description': 'prs_job',
        '/submission': 'prs_res',
        '/match/jobs': 'sml_job',
        '/match/candidates/to/job': 'dis_can',
        '/match/resumes/to/resume': 'sgt_can',
        '/match/jobs/resume': 'sgt_job',
        '/compare/candidates': 'cmp_can',
        '/search/candidate/resume': 'get_res',
        '/search/parsed/resume': 'get_res',
        '/search/parsed/jobs': 'get_job',
        '/search/jobs/resumes': 'src_job',
        '/score/by/id': 'sco_res',
        '/parse/resume-text': 'prs_res1',
        '/parse/resume': 'prs_res',
        '/delete/resume': 'prs_res',
        '/delete/job': 'prs_job',
        '/parse/profile': 'prs_res',
        '/parsing/stats': 'srv_prs',
        '/audit/stats': 'tol_sov',
        '/profile/category/weights': 'set_wgts',
    }
    if service_name in endpoints:
        return endpoints[service_name]


def user_serv_perm(request, clt_id: str, field: str) -> bool:
    """
    Check for Permission to User with Service Name
    """
    active_model = CltRegSchema()
    user_data = active_model.get_client_info(request, clt_id).to_json()
    user_data = json.loads(user_data)
    if user_data.get(field):
        return True


def send_mail_simplify_hire(request, client_name: str, client_id: str, score: list):
    subject = common_config.common_url_settings.get("SUBJECT")

    value = common_config.common_url_settings.get("MESSAGE").format(client_name, client_id, score)
    request.app.logger.info("Mail content is %s" % value )
    message = emails.html(
        html=value,
        subject=subject,
        mail_from=common_config.common_url_settings.get("FROM_EMAIl"),
        cc=common_config.common_url_settings.get("CC_EMAIL")
    )

    # Send the email
    response = message.send(
        to=common_config.common_url_settings.get("TO_EMAIL"),
        smtp={
            "host": config.host,
            "port": config.port,
            "user": config.user,
            "password": config.password,
            "tls": True,
        },
    )
    if response.status_code == 250:
        request.app.logger.error("Email Success Response {}".format(response))
        result = {
            "code": HTTP_200_OK,
            "message": common_config.common_url_settings.get("EMAIL_SUCCESS_MSG")
        }
    else:
        request.app.logger.error("Email Error Response {}".format(response))
        result = {
            "code": HTTP_400_BAD_REQUEST,
            "message": common_config.common_url_settings.get("EMAIL_FAIL_MSG")
        }
    return result
