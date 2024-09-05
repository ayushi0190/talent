# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Miscellaneous helper methods
@author <rchakraborty@simplifyvms.com>
@author <sreddy@simplifyvms.com>
@author <ankits@simplifyvms.com>
@author <satya@simplifyvms.com>
"""
import hashlib
import random
import string
from fastapi import Request, APIRouter
from bs4 import BeautifulSoup
import uuid
import time
from datetime import datetime


from src.admin.config.admin_configs import common_adm_settings
from src.db.crud.admin.clt_reg_schema import CltRegSchema
from src.services.common.config.common_config import common_url_settings
from src.services.common.validations.job_parse_by_id_validations import JobParseByIdValidations
from src.services.common.validations.parse_resume_validations import ParseResumeValidations
from src.services.common.validations.score_by_id_validations import ScoreByIdValidations
from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from src.db.crud.sovren.intern_res_schema import InternResSchema


def find_words_exists(word_list: list, actual_string: str) -> bool:
    """
    Find words exists or not
    :param word_list: List
    :param actual_string: String
    :return:
    """
    if actual_string in word_list:
        return True
    return False


def get_job_board_headers() -> dict:
    """
    Get Job board headers
    :return:
    """
    header = {
        "Content-Type": "application/json",
        "Authorization": common_url_settings.get("JOB_BOARD_AUTHORIZATION"),

    }
    return header


def filter_string_inputs(data: str) -> str:
    """
    Filter input string by removing escape characters
    :param data:
    :return:
    """
    filter_elements = ''.join([chr(i) for i in range(1, 32)])
    return data.translate(str.maketrans('', '', filter_elements))


def remove_special_characters(data: str) -> str:
    """
    Remove all special characters from
    :param data:
    :return:
    """
    return ''.join(e for e in data if e.isalnum())


def filter_xss(data: str, remove_html: bool = False) -> BeautifulSoup:
    """
    Filter XSS attacks
    :param remove_html:
    :param data:
    :return:
    """
    soup = BeautifulSoup(data, "lxml")
    # Remove <script> tag
    for ele in soup.select('script'):
        ele.extract()
    # Remove html contents tag
    if remove_html:
        soup = soup.text
    return soup


def get_formatted_job_data(data: JobParseByIdValidations) -> dict:
    """
    Formatted data for jobs by id validation
    :param data:
    :return:
    """
    return {
        "job_id": data.job_id
    }



def get_formatted_score_data(data: ScoreByIdValidations) -> dict:
    """
    Formatted data for jobs by id validation
    :param data:
    :return:
    """
    return {
        "job_id": data.job_id,
        "resume_id": data.resume_id
    }

def get_formatted_resume(data: ParseResumeValidations) -> dict:
    """
    Formatted data for resumes
    :param data:
    :return:
    """
    data = data.dict()
    return {
        "document_as_base_64_string": data.get('document_as_base_64_string'),
        "index_id": data.get('index_id'),
        "resume_document_id": data.get('resume_document_id',''),
        "resume_id": data.get('resume_id','')
    }


def get_hire_score_format(data, matching_records, parser_type):
    """
    Client score format
    :param data:
    :param matching_records:
    :param parser_type:
    :return:
    """
    common_format = {}
    common_format.update({
        "score": {
            'WeightedScore': data.get("WeightedScore", 0),
            'UnweightedCategoryScores': data.get("UnweightedCategoryScores", None),
            'ReverseCompatibilityScore': data.get("ReverseCompatibilityScore", 0),
            'SuggestedCategoryWeights': matching_records. \
                get("SuggestedCategoryWeights", None),
            'AppliedCategoryWeights': matching_records. \
                get("AppliedCategoryWeights", None),
            'resume_id': data.get('resume_id'),
            'response_id': data.get('response_id'),
            'job_reference_number': data.get('job_reference_number'),
            'parser_type': parser_type}
    })
    return common_format



def get_vms_score_format(data, matching_records, parser_type, input_data):
    """
    Client score format
    :param data:
    :param matching_records:
    :param parser_type:
    :return:
    """
    common_format = {}
    common_format.update({
            "job_id": input_data.get('job_id', None),
            "resume": input_data.get('resume', None),
            "first_name": input_data.get('first_name', None),
            "response_id": input_data.get('response_id', None),
            "last_name": input_data.get('last_name', None),
            "great_match": None,
            "email": input_data.get('email', None),
            "isProcessed": True,
            "created_at": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'),
            "vendor": input_data.get('vendor', None),
            "score": data.get('WeightedScore', 0),
            "score_json": {
                    'Id': data.get('Id'),
                    'WeightedScore': data.get('WeightedScore', 0),
                    'UnweightedCategoryScores':
                        data.get('UnweightedCategoryScores', None),
                    'ReverseCompatibilityScore':
                        data.get('ReverseCompatibilityScore', 0),
                    'IndexId': data.get('IndexId')
                },

            "question_answers": input_data.get('question_answers', None),
            "parse_resume_status_code": input_data.get('parse_resume_status_code', None)

            })
    return common_format


def generate_resume_bucket(request, client_id: str) -> str:
    """
    Generate resume bucket of client
    :param request:
    :param client_id:
    :return:
    """
    if client_id is None:
        return ''
    auth_schema = CltRegSchema()
    client_name = auth_schema.get_client_name_by_id(request, client_id)
    client_abbrv = None
    if client_name:
        filtered_client_name = remove_special_characters(client_name)
        if len(filtered_client_name) > common_adm_settings.get("MAX_CHARS_IN_CLT_ID"):
            client_abbrv = filtered_client_name[0:common_adm_settings.get("MAX_CHARS_IN_CLT_ID")].upper()
        else:
            client_abbrv = filtered_client_name[0:len(filtered_client_name)].upper()

    rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8)).upper()
    client_server_name = client_abbrv + rand_str
    return common_adm_settings.get("CLIENT_BASE_RESUME_INDEX") + client_server_name


def generate_job_bucket(request, client_id: str) -> str:
    """
    Generate job bucket of client
    :param request:
    :param client_id:
    :return:
    """
    if client_id is None:
        return ''
    auth_schema = CltRegSchema()
    client_name = auth_schema.get_client_name_by_id(request, client_id)
    client_abbrv = None
    if client_name:
        filtered_client_name = remove_special_characters(client_name)
        if len(filtered_client_name) > common_adm_settings.get("MAX_CHARS_IN_CLT_ID"):
            client_abbrv = filtered_client_name[0:common_adm_settings.get("MAX_CHARS_IN_CLT_ID")].upper()
        else:
            client_abbrv = filtered_client_name[0:len(filtered_client_name)].upper()

    rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8)).upper()
    client_server_name = client_abbrv + rand_str
    return common_adm_settings.get("CLIENT_BASE_JOB_INDEX") + client_server_name


def generate_resume_doc_id(base_64_encoded_str: str) -> str:
    """
    Generate resume document id and MD5 hash of passed resume base 64
    :param base_64_encoded_str:
    :return: MD5 Hash and Resume Doc ID
    """

    # Generate UUID for the resume
    resume_doc_id = uuid.uuid4()
    return resume_doc_id


def generate_resume_md5(base_64_encoded_str: str) -> str:
    """
    Generate resume document id and MD5 hash of passed resume base 64
    :param base_64_encoded_str:
    :return: MD5 Hash and Resume Doc ID
    """
    # Get the Hexadecimal of resume base 64
    md5_hash = hashlib.md5(base_64_encoded_str.encode()).hexdigest()

    return md5_hash



def create_resume_id(index_id: str) -> dict:
    """
    Resume Id Creation
    :param index_id:
    :return:
    """
    timestamp = int(time.time())
    random_num = random.randint(100, 100000)
    res_inf = "-".join(index_id.split('-')[0:2])
    ext_name = index_id.split('-')[2]
    clt_name = index_id.split('-')[-1]
    resume_id = res_inf + '-' + str(timestamp) + '-' + ext_name + '-' + clt_name + '-' + str(random_num)
    return resume_id


def get_authorized_services(request):
    """
    Get the services information which client has subscribed
    :param request:
    :return:
    """
    auth_schema = CltRegSchema()
    client_id = request.headers["client_id"]
    # Get Tool info based on client ID
    service_info = auth_schema.get_client_info(request, client_id)
    return service_info

def check_and_create_resume_id(md5_hash, client_id, index_id, orig_doc_md5,
                               additional_skills):
    '''Create common resume_doc_id, resume_id.
    This will be used when this md5_hash is not found in DB'''
    res_schema = PrsResInfSchema()
    doc_base64 = ''
    doc_md5 = md5_hash
    if additional_skills:
        res_info = res_schema.get_by_hash_and_skills(orig_doc_md5, client_id,
                                                 additional_skills)
        if res_info:
            if res_info.clt_id == client_id:
                resume_doc_id = res_info.res_doc_id
                resume_id = res_info.res_id
                doc_base64 = res_info.res_b64
                doc_md5 = res_info.doc_md5
            else:
                resume_doc_id = res_info.res_doc_id
                resume_id = create_resume_id(index_id)
                doc_base64 = res_info.res_b64
                doc_md5 = res_info.doc_md5
        else:
            resume_doc_id = generate_resume_doc_id(None)
            resume_id = create_resume_id(index_id)
            doc_md5 = ''
    else:
        # Check resume id for client
        res_info = res_schema.get_by_client(md5_hash, client_id)
        if res_info:
            if res_info.clt_id == client_id:
                resume_doc_id = res_info.res_doc_id
                resume_id = res_info.res_id
            else:
                resume_doc_id = res_info.res_doc_id
                resume_id = create_resume_id(index_id)
        else:
            resume_doc_id = generate_resume_doc_id(None)
            resume_id = create_resume_id(index_id)
    new_resume_info = {'md5_hash': doc_md5, 'resume_doc_id': resume_doc_id,
                       'resume_id': resume_id, 'index_id': index_id,
                       'orig_doc_md5': orig_doc_md5, 'doc_base64': doc_base64
                       }
    return new_resume_info


def get_simpai_score_format(data, parser_type):
    """
    Client score format
    :param data:
    :param matching_records:
    :param parser_type:
    :return:
    """
    common_format = {}
    wgt_score = data.get("totalScore", 0)
    wgt_score = round(wgt_score * 100)
    print("simpai WeightedScore : ", wgt_score)
    common_format.update({
        "score": {
            'WeightedScore': wgt_score,
            'UnweightedCategoryScores': get_simpai_unweighted_score(data),
            'ReverseCompatibilityScore': data.get("ReverseCompatibilityScore", 0),
            'SuggestedCategoryWeights': get_simpai_cat_weights(data),
            'AppliedCategoryWeights': get_simpai_cat_weights(data),
            'resume_id': data.get('resume_id'),
            'response_id': data.get('response_id'),
            'job_reference_number': data.get('job_reference_number'),
            'parser_type': parser_type}
    })
    return common_format


def get_simpai_unweighted_score(data):
    result = []
    unwgt_score = data.get('respectiveScores', {})
    result.append({'EDUCATION': unwgt_score.get('education', {})})
    result.append({'EXPERIENCE': unwgt_score.get('experience', {})})
    result.append({'INDUSTRIES': unwgt_score.get('industry', {})})
    result.append({'JOB_TYPE': unwgt_score.get('job_type', {})})
    result.append({'LOCATION': unwgt_score.get('location', {})})
    result.append({'SKILLS': unwgt_score.get('skills', {})})
    result.append({'JOB_TITLES': unwgt_score.get('title', {})})
    return result


def get_simpai_cat_weights(data):
    cat_wgt = []
    wgt = data.get('usedWeights', {})
    # print('wgt', wgt)
    cat_wgt.append({'EDUCATION': wgt.get('education', {}).get('score', 0.0)})
    cat_wgt.append({'EXPERIENCE': wgt.get('experience', {}).get('score', 0.0)})
    cat_wgt.append({'INDUSTRIES': wgt.get('industry', {}).get('score', 0.0)})
    cat_wgt.append({'JOB_TYPE': wgt.get('job_type', {}).get('score', 0.0)})
    cat_wgt.append({'LOCATION': wgt.get('location', {}).get('score', 0.0)})
    cat_wgt.append({'SKILLS': wgt.get('skills', {}).get('score', 0.0)})
    cat_wgt.append({'JOB_TITLES': wgt.get('title', {}).get('score', 0.0)})
    return cat_wgt



