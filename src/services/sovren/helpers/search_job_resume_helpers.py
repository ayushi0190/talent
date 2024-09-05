# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Search Job Resumes helper methods
@author <rchakraborty@simplifyvms.com>
"""
import json
from datetime import datetime, timedelta
from nested_lookup import nested_lookup
import requests
from starlette.status import HTTP_200_OK, HTTP_204_NO_CONTENT

from src.services.common.config.common_config import common_url_settings
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.common.helpers.misc_helpers import find_words_exists
from src.services.sovren.helpers.misc_helpers import get_sovren_headers
from src.services.common.apis.job_board_services import JobBoardServices
from src.db.crud.sovren.mp_tp_res_schema import MpTpResSchema
from src.db.crud.sovren.cnt_frm_tp_schema import CntFrmTpSchema
from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from src.db.crud.sovren.intern_res_schema import InternResSchema
from src.db.crud.sovren.audit_trails_schema import AuditTrailsSchema

def search_job_resume_data(request, response_info, bucket_type, applied_jobs, count):
    """Searching Job or Resumes Based Criteria"""
    response_data = []
    if len(response_info['Value']['Matches']) > 0:
        clt_id = request.headers['client_id']
        audit_model = AuditTrailsSchema()
        service_name = request.url.path
        for data in response_info['Value']['Matches']:
            if bucket_type == "Job":
                if data.get("Id").lower() not in applied_jobs:
                    job_board = JobBoardServices()
                    job_details = job_board.check_job_exist(request, data.get("Id"))
                    if job_details.get('code') == 200:
                        job_details = job_details.get('data')
                    if job_details.get('status-code') == 200:
                        job_details = job_details['result'][0]['job']
                        if job_details.get('job_show_url') is not None \
                                and job_details.get('job_status') == "Y" \
                                and \
                                not (
                                        job_details.get('job_show_url', '').
                                                startswith('http://localhost:')
                                ):
                            job_title = job_details.get('job_title', None)
                            company_name = job_details.get('company_name', None)
                            job_location = job_details.get('job_location', None)
                            job_show_url = job_details.get('job_show_url', None)
                            job_id = data.get('Id', '').upper()
                            data.update({'Id': job_id,
                                         'job_title': job_title,
                                         'company_name': company_name,
                                         'job_location': job_location,
                                         'job_show_url': job_show_url})
                            response_data.append(data)
                            if len(response_data) == count:
                                break
                    else:
                        continue
            else:
                result = wrap_matching_resumes(data)
                if result['Data'] is not None:
                    response_data.append(result)
                if len(response_data) == count:
                    break
        response_data = {
            'code': HTTP_200_OK,
            'results': response_data
        }
        audit_model.add(service_name,clt_id)
        return response_data
    else:
        response = {
            "code": HTTP_204_NO_CONTENT,
            "data": []
        }
        return response

def wrap_matching_resumes(data):
    """Matching Resumes Values"""
    candidate_data = get_candidates_detail_by_id(
        data.get('Id').upper())
    # candidate_data = "Ramesh"
    if candidate_data and len(candidate_data) > 0:
        data = {
            'Id': data.get('Id'),
            'Data': candidate_data
        }
    else:
        data = {
            'Id': data.get('Id'),
            'Data': None
        }
    return data


def custom_all_filters(payload, data):
    """
    Custom filters
    :param payload: dictionary
    :param data: dictionary
    :return: dictionary
    """
    current_date = datetime.today().strftime('%Y-%m-%d')
    date_before_one_month = datetime.today() - timedelta(
        days=int(common_url_settings.get('QUERY_DAYS')))
    if data.get("Titles"):
        payload['FilterCriteria']['JobTitles'] = []
        for i in data.get("Titles"):
            payload['FilterCriteria']['JobTitles']. \
                append({"Title": i, "IsCurrent": True})

    if data.get("Skills"):
        payload['FilterCriteria']['Skills'] = []
        for i in data.get('Skills'):
            payload['FilterCriteria']['Skills'].append(
                {'SkillName': ''. \
                    join(e for e in i if e.isalnum() or e.isspace())})
    if data.get("DocumentIds") is not None:
        payload['FilterCriteria']['DocumentIds'] = data.get("DocumentIds")
    if data.get("SkillsMustAllExist") is True:
        payload['FilterCriteria']['SkillsMustAllExist'] = True
    if data.get("Employers") is not None:
        payload['FilterCriteria']['Employers'] = data.get("Employers")
    if data.get("EmployersMustAllBeCurrentEmployer") is True:
        payload['FilterCriteria']['EmployersMustAllBeCurrentEmployer'] = True
    if data.get('DateRange'):
        payload['FilterCriteria']['RevisionDateRange'] = {}
        payload['FilterCriteria']['RevisionDateRange'].update(
            {'Minimum': data.get('DateRange').get('Minimum',
                                                  date_before_one_month. \
                                                  strftime('%Y-%m-%d')),
             'Maximum': data.get('DateRange'). \
                 get('Maximum', current_date)})
    if data.get("Educations"):
        payload['FilterCriteria']['Educations'] = []
        for i in data.get('Educations'):
            payload['FilterCriteria']['Educations'].append(
                {'SchoolName': i.get('SchoolName', ''),
                 'DegreeMajor': i.get('DegreeMajor', ''),
                 'DegreeName': i.get('DegreeName', ''),
                 'DegreeType': i.get('DegreeType', ''),
                 'MinimumGPA': i.get('MinimumGPA', '0')})
    if data.get('Locations'):
        payload['FilterCriteria']['LocationCriteria'] = {}
        locations = []
        location_details = {
            "CountryCode": data.get('Locations'). \
                get('CountryCode', ""),
            "Region": data.get('Locations'). \
                get('Region', ""),
            "Municipality": data.get('Locations'). \
                get('Municipality', ""),
            "PostalCode": data.get('Locations'). \
                get('PostalCode', ""),
        }
        locations.append(location_details)
        payload['FilterCriteria']['LocationCriteria']['Locations'] = locations
        if data.get('Locations').get('GeoPoint') is not None:
            geo_points = {
                "Latitude": data.get('Locations'). \
                    get('GeoPoint').get('Latitude', ''),
                "Longitude": data.get('Locations'). \
                    get('GeoPoint').get('Longitude', '')
            }
            geo_credentials = {
                "GeocodeProvider": data.get('Locations'). \
                    get('GeocodeProvider', "None"),
                "GeocodeProviderKey": data.get('Locations'). \
                    get('GeocodeProviderKey', "")
            }
            location_details.update({"GeoPoint": geo_points})
            payload['FilterCriteria']['LocationCriteria']. \
                update(geo_credentials)
        if data.get('Locations').get('Distance') is not None:
            distance_data = {
                "Distance": data.get('Locations'). \
                    get('Distance', 0),
                "DistanceUnit": data.get('Locations'). \
                    get('DistanceUnit', "Miles")
            }
            payload['FilterCriteria']['LocationCriteria']. \
                update(distance_data)
    if data.get("SearchExpression") is not None:
        payload['FilterCriteria']['SearchExpression'] = data. \
            get("SearchExpression")
    if data.get("HasPatents") is True:  # for resume only
        payload['FilterCriteria']['HasPatents'] = True
    if data.get("HasSecurityCredentials") is True:  # for resume only
        payload['FilterCriteria']['HasSecurityCredentials'] = True
    if data.get("SecurityCredentials") is not None:  # for resume only
        payload['FilterCriteria']['SecurityCredentials'] = data. \
            get("SecurityCredentials")
    if data.get("IsAuthor") is True:  # for resume only
        payload['FilterCriteria']['IsAuthor'] = True
    if data.get("IsPublicSpeaker") is True:  # for resume only
        payload['FilterCriteria']['IsPublicSpeaker'] = True
    if data.get("IsMilitary") is True:  # for resume only
        payload['FilterCriteria']['IsMilitary'] = True
    if data.get("SchoolNames") is not None:
        payload['FilterCriteria']['SchoolNames'] = data. \
            get("SchoolNames")
    if data.get("DegreeNames") is not None:
        payload['FilterCriteria']['DegreeNames'] = data. \
            get("DegreeNames")
    if data.get("DegreeTypes") is not None:
        payload['FilterCriteria']['DegreeTypes'] = data. \
            get("DegreeTypes")
    if data.get('LanguagesKnown') is not None:
        payload['FilterCriteria']['LanguagesKnown'] = data. \
            get('LanguagesKnown')
    if data.get("LanguagesKnownMustAllExist") is True:
        payload['FilterCriteria']['LanguagesKnownMustAllExist'] = True
    if data.get('CurrentManagementLevel') is not None:
        payload['FilterCriteria']['CurrentManagementLevel'] = data. \
            get('CurrentManagementLevel')
    if data.get("IsTopStudent") is True:  # for resume only
        payload['FilterCriteria']['IsTopStudent'] = True
    if data.get("IsCurrentStudent") is True:  # for resume only
        payload['FilterCriteria']['IsCurrentStudent'] = True
    if data.get("IsRecentGraduate") is True:  # for resume only
        payload['FilterCriteria']['IsRecentGraduate'] = True
    if data.get('DocumentLanguages') is not None:
        payload['FilterCriteria']['DocumentLanguages'] = data. \
            get('DocumentLanguages')
    if data.get('MonthsExperience') is not None:
        payload['FilterCriteria']['MonthsExperience'] = {}
        month_experience = {
            "Minimum": data.get('MonthsExperience').get('Minimum', 0),
            "Maximum": data.get('MonthsExperience').get('Maximum', 0)
        }
        payload['FilterCriteria']['MonthsExperience']. \
            update(month_experience)
    if data.get('MonthsManagementExperience') is not None:
        payload['FilterCriteria']['MonthsManagementExperience'] = {}
        month_management_experience = {
            "Minimum": data.get('MonthsManagementExperience'). \
                get('Minimum', 0),
            "Maximum": data.get('MonthsManagementExperience'). \
                get('Maximum', 0)
        }
        payload['FilterCriteria']['MonthsManagementExperience'].update(
            month_management_experience)
    if data.get('ExecutiveType') is not None:
        payload['FilterCriteria']['ExecutiveType'] = data.get('ExecutiveType')
    if data.get('Certifications') is not None:
        payload['FilterCriteria']['Certifications'] = data.get('Certifications')
    return payload


def get_candidates_detail_by_id(resume_id):
    """
    Get the candidates detail by resume id
    :param resume_id: string
    :return json
    """

    result = {}
    cont_info = CntFrmTpSchema()
    get_contact = cont_info.get(resume_id)
    get_contact_info_from_db = InternResSchema().get(resume_id)
    if get_contact_info_from_db:
        get_candidate = get_contact_info_from_db.resp
        get_candidate = json.loads(get_candidate)
        get_candidate = get_candidate['Value']['ParsedDocument']
        data = json.loads(get_candidate)
        filtered_contacts = get_information_from_document(
            data['Resume']['StructuredXMLResume'])
        get_contact_info_from_db = [get_contact_info_from_db]
    else:
        get_contact_info_from_db = PrsResInfSchema.get_data(resume_id, 'sovren')
        print("{} get_contact_info_from_db :: {}".format(resume_id,get_contact_info_from_db))
        if get_contact_info_from_db:
            get_candidate = get_contact_info_from_db.resp
            get_candidate = json.loads(get_candidate)
            get_candidate = get_candidate['Value']['ParsedDocument']
            data = json.loads(get_candidate)
            filtered_contacts = get_information_from_document(
                data['Resume']['StructuredXMLResume'])
        if get_contact_info_from_db:
            get_contact_info_from_db = [get_contact_info_from_db]
    # data = MapTalentPoolResumeInSovren.get_mapped_data(search)
    data = get_contact_info_from_db
    if data:
        try:
            data = json.loads(data[0].resp)
            data = data['Value']['ParsedDocument']
            data = json.loads(data)
        except:
            data = json.loads(data[0].res)
        if isinstance(data, dict):
            employment_history = {}
            if get_contact is not None:
                common_information = get_information_from_document(get_contact)
            elif get_contact_info_from_db:
                common_information = filtered_contacts
            else:
                common_information = get_information_from_document(
                    data["Resume"]["StructuredXMLResume"])
            # Discard profile's of the candidates where
            # first name and last name is not present
            if not common_information.get("first_name") and \
                    not common_information.get("last_name"):
                pass
            else:
                if not isinstance(data["Resume"]["StructuredXMLResume"] \
                                          ["EmploymentHistory"]["EmployerOrg"], list):
                    candidate_employment_history = data["Resume"]["StructuredXMLResume"][
                        "EmploymentHistory"].get("EmployerOrg", None)
                    education_history = get_educational_information(
                        data["Resume"]["StructuredXMLResume"].get("EducationHistory"))
                    for count, ele in enumerate(candidate_employment_history):
                        history = get_employment_information(ele)
                        position_history = get_position_history(
                            ele.get("PositionHistory")[0])
                        employment_history.update({
                            count: {'Organization': history.get("org"),
                                    'JobTitle': position_history.get("title"),
                                    'StartDate': position_history.get("start_date"),
                                    'EndDate': position_history.get("end_date")
                                    }
                        })
                    result.update({
                        'Name': common_information.get('first_name', '') + ' ' + \
                                common_information.get('last_name', ''),
                        'Address': common_information.get('city', '') + ', ' + \
                                   common_information.get('country_code', ''),
                        'DegreeName': education_history.get("degree_name"),
                        'DegreeMajor': education_history.get("degree"),
                        'Institution': education_history.get("institution"),
                        'Email': common_information.get('email'),
                        'Telephone': common_information.get('phone'),
                        'Experience': employment_history
                    })
                else:
                    candidate_employment_history = data["Resume"]["StructuredXMLResume"] \
                        ["EmploymentHistory"]["EmployerOrg"]

                    education_history = get_educational_information(
                        data["Resume"]["StructuredXMLResume"].get("EducationHistory"))
                    for count, ele in enumerate(candidate_employment_history):
                        history = get_employment_information(ele)
                        position_history = get_position_history(
                            ele.get("PositionHistory")[0])
                        employment_history.update({
                            count: {'Organization': history.get("org"),
                                    'JobTitle': position_history.get("title"),
                                    'StartDate': position_history.get("start_date"),
                                    'EndDate': position_history.get("end_date")
                                    }
                        })
                    result.update({
                        'Name': common_information.get('first_name', '') + ' ' + \
                                common_information.get('last_name', ''),
                        'Address': common_information.get('city', '') + ', ' + \
                                   common_information.get('country_code', ''),
                        'DegreeName': education_history.get("degree_name"),
                        'DegreeMajor': education_history.get("degree"),
                        'Institution': education_history.get("institution"),
                        'Email': common_information.get('email'),
                        'Telephone': common_information.get('phone'),
                        'Experience': employment_history
                    })
        return result
    else:
        new_data = get_document_from_sovern(resume_id)
        if new_data.get('value') == []:
            data = []
        else:
            data = json.loads(new_data.get('value'))
        if isinstance(data, dict):
            employment_history = {}
            if get_contact is not None:
                common_information = get_information_from_document(get_contact)
            elif get_contact_info_from_db:
                common_information = filtered_contacts
            else:
                common_information = get_information_from_document(data["Resume"] \
                                                                        ["StructuredXMLResume"])
            # Discard profile's of the candidates where
            # first name and last name is not present
            if not common_information.get("first_name") and \
                    not common_information.get("last_name"):
                pass
            else:
                if not isinstance(data["Resume"]["StructuredXMLResume"] \
                                          ["EmploymentHistory"]["EmployerOrg"], list):
                    candidate_employment_history = data["Resume"]["StructuredXMLResume"] \
                        ["EmploymentHistory"].get("EmployerOrg", None)
                    education_history = get_educational_information(
                        data["Resume"]["StructuredXMLResume"].get("EducationHistory"))
                    for count, ele in enumerate(candidate_employment_history):
                        history = get_employment_information(ele)
                        position_history = get_position_history(ele.get("PositionHistory")[0])
                        employment_history.update({
                            count: {'Organization': history.get("org"),
                                    'JobTitle': position_history.get("title"),
                                    'StartDate': position_history.get("start_date"),
                                    'EndDate': position_history.get("end_date")
                                    }
                        })
                    result.update({
                        'Name': common_information.get('first_name', '') + ' ' + \
                                common_information.get('last_name', ''),
                        'Address': common_information.get('city', '') + ', ' + \
                                   common_information.get('country_code', ''),
                        'DegreeName': education_history.get("degree_name"),
                        'DegreeMajor': education_history.get("degree"),
                        'Institution': education_history.get("institution"),
                        'Email': common_information.get('email'),
                        'Telephone': common_information.get('phone'),
                        'Experience': employment_history
                    })
                else:
                    candidate_employment_history = data["Resume"]["StructuredXMLResume"] \
                        ["EmploymentHistory"]["EmployerOrg"]

                    education_history = get_educational_information(
                        data["Resume"]["StructuredXMLResume"].get("EducationHistory"))
                    for count, ele in enumerate(candidate_employment_history):
                        history = get_employment_information(ele)
                        position_history = get_position_history(
                            ele.get("PositionHistory")[0])
                        employment_history.update({
                            count: {'Organization': history.get("org"),
                                    'JobTitle': position_history.get("title"),
                                    'StartDate': position_history.get("start_date"),
                                    'EndDate': position_history.get("end_date")
                                    }
                        })
                    result.update({
                        'Name': common_information.get('first_name', '') + ' ' + \
                                common_information.get('last_name', ''),
                        'Address': common_information.get('city', '') + ', ' + \
                                   common_information.get('country_code', ''),
                        'DegreeName': education_history.get("degree_name"),
                        'DegreeMajor': education_history.get("degree"),
                        'Institution': education_history.get("institution"),
                        'Email': common_information.get('email'),
                        'Telephone': common_information.get('phone'),
                        'Experience': employment_history
                    })
        return result


def get_document_from_sovern(resume_id):
    """
    Get a document information from Sovren
    :param document_id:
    :return:
    """
    resume_index_to_search = resume_id.split("-")
    resume_index = resume_index_to_search[0] + '-' + resume_index_to_search[1] + '-' + \
                   resume_index_to_search[3] + '-' + resume_index_to_search[4]
    resume_indexes = ["simp-r-ex-intern", "SIMP-R-EX-INTERN",
                      "SIMP-R-CAREER-X", "SIMP-R-SVMS-X", "simp-r-career-x", "simp-r-svms-x"]
    if find_words_exists(resume_indexes, resume_index):
        resume_index = common_url_settings.get(
            "INTERNAL_BUCKET")
    request_url = sovren_url_settings.get("SOVREN_CREATE_INDEX_URL") + resume_index + \
                  '/documents/' + resume_id
    response = requests.request("GET", request_url, headers=get_sovren_headers())
    if response.status_code == 200:
        response_info = json.loads(json.dumps(response.json()))
        expected_data = {
            'code': response.status_code,
            'value': response_info['Value']
        }

    else:
        expected_data = {
            'code': response.status_code,
            'value': []
        }

    return expected_data


def get_information_from_document(document_to_search,
                                  keys=["GivenName", "FamilyName", "InternetEmailAddress",
                                        "FormattedNumber", "Municipality", "CountryCode"]):
    """
    Get information from document
    :param document_to_search:
    :param keys:
    :return:
    """

    info = {}
    tmp_infos = []
    for k in keys:
        results = nested_lookup(key=k, document=document_to_search, with_keys=True)
        tmp_infos.append(results)
    for tmp_info in tmp_infos:
        if tmp_info.get('FormattedNumber', None):
            info['phone'] = tmp_info.get("FormattedNumber")[0]
        if tmp_info.get('InternetEmailAddress', None):
            info['email'] = tmp_info.get("InternetEmailAddress")[0]
        if tmp_info.get('GivenName', None):
            info['first_name'] = tmp_info.get("GivenName")[0]
        if tmp_info.get('FamilyName', None):
            info['last_name'] = tmp_info.get("FamilyName")[0]
        if tmp_info.get('Municipality', None):
            info['city'] = tmp_info.get("Municipality")[0]
        if tmp_info.get('CountryCode', None):
            info['country_code'] = tmp_info.get("CountryCode")[0]
    return info


def get_educational_information(document_to_search,
                                keys=["DegreeMajor", "DegreeName", "School"]):
    """
    Get educational information
    :param document_to_search:
    :param keys:
    :return:
    """

    info = {}
    tmp_infos = []
    for k in keys:
        results = nested_lookup(key=k, document=document_to_search, with_keys=True)
        tmp_infos.append(results)
    for tmp_info in tmp_infos:
        if tmp_info.get('DegreeName', None):
            info['degree_name'] = tmp_info.get("DegreeName")[0]
        if tmp_info.get('DegreeMajor', None):
            info['degree'] = tmp_info.get("DegreeMajor")
        if tmp_info.get('School', None):
            info["institution"] = tmp_info.get("School")[0]
    return info


def get_employment_information(document_to_search,
                               keys=["EmployerOrgName"]):
    """
    Get employment information
    :param document_to_search:
    :param keys:
    :return:
    """

    info = {}
    tmp_infos = []
    for k in keys:
        results = nested_lookup(key=k, document=document_to_search, with_keys=True)
        tmp_infos.append(results)
    for tmp_info in tmp_infos:
        if tmp_info.get('EmployerOrgName', None):
            info['org'] = tmp_info.get("EmployerOrgName")
    return info


def get_position_history(document_to_search):
    """
    Get position history
    :param document_to_search:
    :return:
    """
    info = {}
    if document_to_search.get("Title", None):
        info["title"] = document_to_search.get("Title")
    if document_to_search.get("StartDate", None):
        info["start_date"] = document_to_search.get("StartDate")
    if document_to_search.get("EndDate", None):
        info["end_date"] = document_to_search.get("EndDate")
    return info
