# -*- coding: utf-8 -*-
import json
import requests
from starlette import status

from src.services.common.config.common_config import common_url_settings
from src.services.common.helpers.api_helper import connect_to_api
from src.utilities.custom_logging import cust_logger as logger


def append_to_pdf(doc_base64: str, additional_skills: list) -> dict:
    """
    Append additional skills to resume file
    :param : doc_base64
    :param : additional_data
    :return
    """
    msg_list = {'success': 'Skills successfully appended to file',
                'fail': 'Failed to append Skills to file',
                'error': 'Error while appending Skills to file'
                }
    header = {"Content-Type": "application/json"}
    payload = {"doc_base64": doc_base64,
               "additional_data": {"skills": additional_skills}
               }
    result = connect_to_api(header, payload,
                            common_url_settings.get("PDF_EDITOR_API"),
                            'pdf_editor', msg_list)
    return result
