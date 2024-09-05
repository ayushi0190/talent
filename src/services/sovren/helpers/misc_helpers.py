# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Miscellaneous helper methods
@author <rchakraborty@simplifyvms.com>
"""
from datetime import datetime, timedelta
import json
import requests
import arrow
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, \
    HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR

from src.db.crud.sovren.cnt_frm_tp_schema import CntFrmTpSchema
from src.services.common.validations.job_parse_by_description_validations import JobParseByDescriptionValidations
from src.services.sovren.config.sovren_config import sovren_url_settings
from src.services.common.config.common_config import common_url_settings
from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from src.config import config



def data_to_save(job_id: str, name: str, first_name: str,
                 last_name: str, email: str, phone: str,
                 resume: str, vendor: str, response_id: str,
                 resume_id: str, resume_document_id: str,
                 job_index_id: str, resume_index_id: str,
                 resume_standard: str, score_generated: int,
                 question_answers: str):
    """
    Prepare data to save in collection
    :param job_id: String
    :param name: String
    :param first_name: String
    :param last_name: String
    :param email: String
    :param phone: String
    :param resume: String
    :param vendor: String
    :param response_id: String
    :param resume_id: String
    :param resume_document_id: String
    :param job_index_id: String
    :param resume_index_id: String
    :param resume_standard: String
    :param score_generated: String
    :param question_answers: String
    :return: dict
    """
    data = {}
    data.update({
        "job_idx_id": job_index_id,
        "job_id": job_id,
        "res_idx_id": resume_index_id,
        "phone": phone,
        "email": email,
        "resume": resume,
        "vendor": vendor,
        "resp_id": response_id,
        "f_name": first_name,
        "l_name": last_name,
        "name": name,
        "res_doc_id": resume_document_id,
        "res_std": resume_standard,
        "score_gen": score_generated,
        "ques_ans": question_answers,
        "res_id": resume_id

    })
    return data


def error_parsing_resume() -> dict:
    """
    Error in parsing resume
    :return:
    """
    extracted_data = {}
    extracted_data.update({
        'code': HTTP_400_BAD_REQUEST,
        'message': 'Unable to parse resume'
    })
    return extracted_data


def error_in_resume_doc_id() -> dict:
    """
    Error in resume_document_id
    :return:
    """
    extracted_data = {}
    extracted_data.update({
        'code': HTTP_400_BAD_REQUEST,
        'message': 'Resume document id not present'
    })
    return extracted_data


def error_in_indexing_result() -> dict:
    """
    Error in indexing result
    :return:
    """
    extracted_data = {}
    extracted_data.update({
        'code': HTTP_404_NOT_FOUND,
        'message': 'Unable to perform operation, ' +
                   'unable to create new index'
    })
    return extracted_data


def check_job_board_result(status_code: str) -> dict:
    """
    Check job board result
    :param status_code: String
    :return:
    """
    extracted_data = {}
    if status_code != HTTP_200_OK:
        extracted_data.update({
            'code': HTTP_404_NOT_FOUND,
            'message': 'Unable to perform operation, ' +
                       'job id not found'

        })
    return extracted_data


def validate_resume_fields(index_id: str, document_as_base_64_string: str,
                           resume_id: str, resume_document_id: str, job_id: str) -> dict:
    """
    Validate resume parsing fields
    :param index_id:
    :param document_as_base_64_string:
    :param resume_id:
    :param resume_document_id:
    :param job_id:
    :return:
    """
    extracted_data = {}
    if index_id is None:
        extracted_data.update({
            'code': HTTP_400_BAD_REQUEST,
            'message': 'Unable to perform operation, index id not given'

        })

    if document_as_base_64_string is None:
        extracted_data.update({
            'code': HTTP_400_BAD_REQUEST,
            'message': 'Unable to perform operation, base 64 encoded document not given'

        })

    if resume_id is None:
        extracted_data.update({
            'code': HTTP_400_BAD_REQUEST,
            'message': 'Unable to perform operation, resume id not given'

        })

    if resume_document_id is None:
        extracted_data.update({
            'code': HTTP_400_BAD_REQUEST,
            'message': 'Unable to perform operation, resume document id not given'

        })

    if job_id is None:
        extracted_data.update({
            'code': HTTP_400_BAD_REQUEST,
            'message': 'Unable to perform operation, job id not given'

        })
    return extracted_data


def get_job_index(job_id: str) -> str:
    """
    Get job index id
    :param job_id:
    :return:
    """
    job_index = job_id.split("-")
    return job_index[0] + \
           '-' + \
           'J' + \
           '-' + \
           job_index[2] + \
           '-' + \
           job_index[3]


def get_resume_index(res_id: str) -> str:
    """
    Get resume index id
    :param res_id:
    :return:
    """
    resume_index = res_id.split("-")
    return resume_index[0] + \
           '-' + \
           resume_index[1] + \
           '-' + \
           resume_index[3] + \
           '-' + \
           resume_index[4]


def get_job_index_from_resume(res_id: str) -> str:
    """
    Get job index from resume
    :param res_id:
    :return:
    """
    resume_index = res_id.split("-")
    return resume_index[0] + \
           '-' + \
           'J' + \
           '-' + \
           resume_index[3] + \
           '-' + \
           resume_index[4]


def get_sovren_headers() -> dict:
    """
    Get Sovren header to be called for sovren calling API
    :return:
    """
    print("get_sovren_headers : " ,config.settings.env)
    if config.settings.env in {"PRODUCTION", "AWS_ENV"}:
        header = {
            "accept": "application/json",
            "content-type": "application/json",
            "sovren-accountid": sovren_url_settings.get("SOVREN_ACCOUNT_ID"),
            "sovren-servicekey": sovren_url_settings.get("SOVREN_ACCOUNT_SERVICE_KEY"),
        }
    else:
        header = {
            "accept": "application/json",
            "content-type": "application/json",
            "sovren-accountid": sovren_url_settings.get("SOVREN_ACCOUNT_ID"),
            "sovren-servicekey": sovren_url_settings.get("SOVREN_ACCOUNT_SERVICE_KEY"),
        }
    return header


def serialize_job_ref(job_id: str) -> dict:
    """
    Serialize job_document_id
    :param job_id: String
    :return: Dict
    """
    if len(job_id) > 0:
        split_data = job_id.split("-")
    return {
        "sor_sys": split_data[0],
        "sor_tp": split_data[1],
        "sor_prod": split_data[2],
        "clt_job_id": split_data[3],
        "job_brd_id": split_data[4],
    }


def filter_fields_listing(data: dict):
    """
    Seggrate filter fields
    """
    if not isinstance(data, dict):
        data = data.dict()
    type_list = (str, list, tuple, dict)
    int_data = {k: v for k, v in data.items() if isinstance(v, int)}

    data = {k: v for k, v in data.items() if isinstance(v, type_list) if len(v) >= 1}
    data.update(int_data)
    data = {k: data[k] for k in data if data[k] is not False}
    return data


def data_with_no_of_matches(result: list, data: dict):
    """
    For returning the specified number of matches
    """
    if data.get("no_of_matches"):
        count = data.get("no_of_matches")
    else:
        count = 20
    return result[:count]


def custom_all_filters(payload: dict, data: dict) -> dict:
    """
    Custom filters for Payload
    :param payload:
    :param data:
    :return:
    """
    current_date = datetime.today().strftime('%Y-%m-%d')
    date_minimum = datetime.today() - timedelta(
        days=data.refresh_rate)
    if data.Titles and data.Titles != 'string':
        payload['FilterCriteria']['JobTitles'] = []
        for i in data.Titles:
            payload['FilterCriteria']['JobTitles']. \
                append({"Title": i, "IsCurrent": True})
    if data.Skills:
        if data.Skills[0] and data.Skills[0] != 'string':
            payload['FilterCriteria']['Skills'] = []
            for i in data.Skills:
                payload['FilterCriteria']['Skills'].append(
                    {'SkillName': ''. \
                        join(e for e in i if e.isalnum() or e.isspace())})
    if data.resume_id is not None:
        payload['FilterCriteria']['DocumentIds'] = data.resume_id
    if data.SkillsMustAllExist is True:
        payload['FilterCriteria']['SkillsMustAllExist'] = True
    if data.Employers and data.Employers[0] != 'string':
        payload['FilterCriteria']['Employers'] = data.Employers
    if data.EmployersMustAllBeCurrentEmployer is True:
        payload['FilterCriteria']['EmployersMustAllBeCurrentEmployer'] = True
    if data.DateRange:
        maximum = data.DateRange.Maximum if data.DateRange.Maximum \
                                            and data.DateRange.Maximum != 'string' else current_date
        minimum = data.DateRange.Minimum if data.DateRange.Minimum \
                                            and data.DateRange.Minimum != 'string' else date_minimum. \
            strftime('%Y-%m-%d')
        payload['FilterCriteria']['RevisionDateRange'] = {}
        payload['FilterCriteria']['RevisionDateRange'].update(
            {'Minimum': maximum,
             'Maximum': minimum})
    if data.Educations:
        if data.Educations[0] and data.Educations[0] != 'string':
            payload['FilterCriteria']['Educations'] = []
            for i in data.Educations:
                school_name = i.SchoolName if i.SchoolName \
                                              and i.SchoolName != 'string' else ""
                degree_major = i.DegreeMajor if i.DegreeMajor \
                                                and i.DegreeMajor != 'string' else ""
                degree_name = i.DegreeName if i.DegreeName \
                                              and i.DegreeName != 'string' else ""
                degree_type = i.DegreeType if i.DegreeType \
                                              and i.DegreeType != 'string' else ""
                if school_name:
                    payload['FilterCriteria']['Educations'].append(
                        {'SchoolName': school_name})
                if degree_major:
                    payload['FilterCriteria']['Educations'].append(
                        {'DegreeMajor': degree_major})
                if degree_name:
                    payload['FilterCriteria']['Educations'].append(
                        {'DegreeName': degree_name})
                if degree_type:
                    payload['FilterCriteria']['Educations'].append(
                        {'DegreeType': degree_type})
                if i.MinimumGPA >= 0:
                    payload['FilterCriteria']['Educations'].append(
                        {'MinimumGPA': i.MinimumGPA})
    if data.LocationCriteria:
        if data.LocationCriteria.Locations[0] \
                and data.LocationCriteria.Locations[0] != 'string':
            payload['FilterCriteria']['LocationCriteria'] = {}
            locations = []
            location = data.LocationCriteria.Locations[0]
            country_code = location.CountryCode \
                if location.CountryCode and location.CountryCode != 'string' else ""
            region = location.Region \
                if location.Region and location.Region != 'string' else ""
            municipality = location.Municipality \
                if location.Municipality and location.Municipality != 'string' else ""
            postal_code = location.PostalCode \
                if location.PostalCode and location.PostalCode != 'string' else ""
            location_details = {
                "CountryCode": country_code,
                "Region": region,
                "Municipality": municipality,
                "PostalCode": postal_code,
            }
            locations.append(location_details)
            payload['FilterCriteria']['LocationCriteria']['Locations'] = locations
            if location.Geopoint is not None:
                geo_point = location.Geopoint
                geo_points = {
                    "Latitude": geo_point.Latitude,
                    "Longitude": geo_point.Longitude
                }
                geo_credentials = {}
                if data.LocationCriteria.GeocodeProvider is not None \
                        and data.LocationCriteria.GeocodeProvider != 'string':
                    geo_credentials.update({
                        "GeocodeProvider": data.LocationCriteria.GeocodeProvider
                    })
                if data.LocationCriteria.GeocodeProviderKey is not None \
                        and data.LocationCriteria.GeocodeProviderKey != 'string':
                    geo_credentials.update({
                        "GeocodeProviderKey": data.LocationCriteria.GeocodeProviderKey
                    })
                location_details.update({"GeoPoint": geo_points})
                payload['FilterCriteria']['LocationCriteria']. \
                    update(geo_credentials)
            distance_data = {}
            if data.LocationCriteria.Distance is not None:
                distance_data.update({
                    "Distance": data.LocationCriteria.Distance
                })
            if data.LocationCriteria.DistanceUnit \
                    and data.LocationCriteria.DistanceUnit != 'string':
                distance_data.update({
                    "DistanceUnit": data.LocationCriteria.DistanceUnit
                })
            else:
                distance_data.update({
                    "DistanceUnit": "Miles"
                })
                payload['FilterCriteria']['LocationCriteria']. \
                    update(distance_data)
    if data.SearchExpression is not None and data.SearchExpression != 'string':
        payload['FilterCriteria']['SearchExpression'] = data.SearchExpression
    if data.SchoolNames is not None and data.SchoolNames[0] != 'string':
        payload['FilterCriteria']['SchoolNames'] = data.SchoolNames
    if data.DegreeNames is not None and data.DegreeNames[0] != 'string':
        payload['FilterCriteria']['DegreeNames'] = data.DegreeNames
    if data.DegreeTypes is not None and data.DegreeTypes[0] != 'string':
        payload['FilterCriteria']['DegreeTypes'] = data.DegreeTypes
    if data.LanguagesKnown is not None and data.LanguagesKnown[0] != 'string':
        payload['FilterCriteria']['LanguagesKnown'] = data.LanguagesKnown
    if data.LanguagesKnownMustAllExist is True:
        payload['FilterCriteria']['LanguagesKnownMustAllExist'] = data.LanguagesKnownMustAllExist
    if data.CurrentManagementLevel is not None and data.CurrentManagementLevel != 'string':
        payload['FilterCriteria']['CurrentManagementLevel'] = data.CurrentManagementLevel
    if data.DocumentLanguages is not None and data.DocumentLanguages[0] != 'string':
        payload['FilterCriteria']['DocumentLanguages'] = data.DocumentLanguages
    if data.MonthsExperience is not None:
        payload['FilterCriteria']['MonthsExperience'] = {}
        month_experience = {
            "Minimum": data.MonthsExperience.Minimum,
            "Maximum": data.MonthsExperience.Maximum
        }
        payload['FilterCriteria']['MonthsExperience']. \
            update(month_experience)
    if data.MonthsManagementExperience is not None:
        payload['FilterCriteria']['MonthsManagementExperience'] = {}
        month_management_experience = {
            "Minimum": data.MonthsManagementExperience.Minimum,
            "Maximum": data.MonthsManagementExperience.Maximum
        }
        payload['FilterCriteria']['MonthsManagementExperience'].update(
            month_management_experience)
    if data.ExecutiveType is not None and data.ExecutiveType[0] != 'string':
        payload['FilterCriteria']['ExecutiveType'] = data.ExecutiveType
    if data.Certifications is not None and data.Certifications[0] != 'string':
        payload['FilterCriteria']['Certifications'] = data.Certifications
    return payload


def format_job_description_request(data: JobParseByDescriptionValidations) -> dict:
    """
    Format job description request
    :param data:
    :return:
    """
    location_info = data.work_location[0]
    country = location_info.country if location_info.country and location_info.country != 'string' else "USA"
    city = location_info.city if location_info.city and location_info.city != 'string' else ""
    state = location_info.state if location_info.state and location_info.state != 'string' else ""
    zip = location_info.zip if location_info.zip and location_info.zip != 'string' else ""
    location_details = {
        "country": country,
        "city": city,
        "state": state,
        "zip": zip
    }

    result_data = {
        "job_title": data.job_title,
        "job_description": data.job_description.strip(),
        "client_name": data.client_name,
        "work_locations": "{}",
        "work_locations_ex": location_details

    }
    return result_data


def get_parsed_education(data):
    """
    Get parsed education information
    :param data:
    :return:
    """
    edu_details = []

    edu_hist = data.get("EducationHistory", {})
    if edu_hist:
        school_info = edu_hist.get("SchoolOrInstitution", [])

        for edu_info in school_info:
            degDate = ''
            degName = ''
            deg_major_val = ''
            institution = ''

            school = edu_info.get('School', '')

            for val in school:
                get_institution = val.get('SchoolName', '')
                if get_institution:
                    institution = get_institution

            degree = edu_info.get('Degree', '')
            for key in degree:
                get_degName = key.get('DegreeName', '')
                if get_degName:
                    degName = get_degName

                degree_major = key.get('DegreeMajor', '')

                for deg in degree_major:
                    deg_major_name = deg.get('Name', '')
                    if deg_major_name:
                        deg_major_val = deg_major_name[0]

                deg_date = key.get('DegreeDate', {})
                if deg_date:
                    degDate = deg_date.get('YearMonth', deg_date.get('Year', {}))

            result = {}
            if degName:
                result["Name"] = degName
            if deg_major_val:
                result["Degree Major"] = deg_major_val
            if degDate:
                result["Degree Date"] = degDate
            if institution:
                result["Institution"] = institution

            edu_details.append(result)
    return edu_details


def get_parsed_experience(data):
    """
    Get experience of the candidate
    :param data:
    :return:
    """
    exp_details = []

    emp_hist = data.get("EmploymentHistory", {})
    if emp_hist:
        emp_org_info = emp_hist.get("EmployerOrg", [])

        for org_info in emp_org_info:
            org_name = org_info.get('EmployerOrgName', '')
            position_history = org_info.get("PositionHistory", [])
            title = ''
            start_date = ''
            end_date = ''
            position_type = ''

            for key in position_history:
                get_title = key.get('Title', '')
                if get_title:
                    title = get_title
                get_postion_type = key.get('@positionType', '')
                if get_postion_type:
                    position_type = get_postion_type
                get_start_date = key.get('StartDate', '').get('YearMonth', key.get('StartDate', '').get('AnyDate', ''))
                if get_start_date:
                    start_date = get_start_date
                get_end_date = key.get('EndDate', '').get('YearMonth', key.get('EndDate', '').get('StringDate', '')) \
                    if key.get('EndDate') else None
                if get_end_date:
                    end_date = get_end_date

            result = {}
            if org_name:
                result['Organization Name'] = org_name
            if title:
                result['Title'] = title
            if start_date:
                result['Start Date'] = start_date
            if end_date:
                result['End Date'] = end_date
            if position_type:
                result['Position Type'] = position_type

            exp_details.append(result)

    return exp_details


def get_work_location(data):
    """
    Get work location of the candidate
    :param data:
    :return:
    """
    work_location = []

    emp_hist = data.get("EmploymentHistory", {})
    if emp_hist:
        emp_org_info = emp_hist.get("EmployerOrg", [])

    for emp_org in emp_org_info:
        org_name = emp_org.get('EmployerOrgName', '')
        position_history = emp_org.get("PositionHistory", [])
        municipality = ''
        region = ''
        country_code = ''
        postion_loc = ''

        for key in position_history:
            org_info = key.get('OrgInfo', [])

            for info in org_info:
                if len(org_info) > 0:
                    postion_loc = info.get('PositionLocation', {})
                    if postion_loc:
                        country_code = postion_loc.get('CountryCode', '')
                        region = postion_loc.get('Region', [])
                        if len(region) > 0:
                            region = region[0]
                        municipality = postion_loc.get('Municipality', '')

        result = {}
        if postion_loc:
            if org_name:
                result['Organisation Name'] = org_name
            if country_code:
                result['Country Code'] = country_code
            if region:
                result['Region'] = region
            if municipality:
                result['Municipality'] = municipality

        work_location.append(result)

    return work_location


def get_certification(data):
    """
    Get certification of candidate
    :param data:
    :return:
    """
    cert_details = []

    certs = data.get("LicensesAndCertifications", {})
    if certs:
        cert_info = certs.get("LicenseOrCertification", [])

        for cert in cert_info:
            cert_name = ''
            cert_name = cert.get('Name', '')

            result = {}
            if cert_name:
                result['Certification Name'] = cert_name

            cert_details.append(result)

    return cert_details


def get_languages(data):
    """
    Get languages known by candidate
    :param data:
    :return:
    """
    language_details = []

    languages = data.get("Languages", {})

    if languages:
        lang_info = languages.get("Language", [])
        for lang in lang_info:
            lang_code = ''
            read = ''
            write = ''
            speak = ''

            language = lang.get('LanguageCode')
            read = lang.get('Read')
            write = lang.get('Write')
            speak = lang.get('Speak')

            result = {}
            if language:
                result['Language'] = language
                if read:
                    result['Read'] = read
                if write:
                    result['Write'] = write
                if speak:
                    result['Speak'] = speak

                language_details.append(result)

    return language_details


def get_all_skills(data):
    """
    Get all skills
    :param data:
    :return:
    """
    all_skills = set()
    taxroot = ''
    data2 = data.get("UserArea", {})
    user_area = data2.get("sov:ResumeUserArea", {})
    if user_area:
        exp_summary = user_area.get("sov:ExperienceSummary")
        if exp_summary:
            skill_taxonomy = exp_summary.get("sov:SkillsTaxonomyOutput", {})
            if skill_taxonomy:
                taxroot = skill_taxonomy.get("sov:TaxonomyRoot", [])

            if taxroot:
                for tax in taxroot:
                    taxonomy = tax.get('sov:Taxonomy', [])
                    if taxonomy:
                        for tax_info in taxonomy:
                            sub_tax = tax_info.get('sov:Subtaxonomy', [])

                            for sub_tax_info in sub_tax:
                                skill = sub_tax_info.get("sov:Skill", [])

                                if skill != None:
                                    for skill_info in skill:
                                        skill_name = skill_info.get('@name', '')
                                        last_used = skill_info.get('@lastUsed')
                                        tot_months = skill_info.get('@totalMonths')

                                        result = {}
                                        if skill_name and (last_used and tot_months):
                                            result = skill_name

                                            all_skills.add(result)

    return list(all_skills)


def get_parsed_skills1(data):
    """
    Get parsed skill set one
    :param data:
    :return:
    """
    skill_details = []
    taxroot = ''
    data2 = data.get("UserArea", {})
    user_area = data2.get("sov:ResumeUserArea", {})
    if user_area:
        exp_summary = user_area.get("sov:ExperienceSummary")
        if exp_summary:
            skill_taxonomy = exp_summary.get("sov:SkillsTaxonomyOutput", {})
            if skill_taxonomy:
                taxroot = skill_taxonomy.get("sov:TaxonomyRoot", [])

    if taxroot:
        for tax in taxroot:
            taxonomy = tax.get('sov:Taxonomy', '')

            if taxonomy:
                for tax_info in taxonomy:
                    tax_name = tax_info.get('@name', '')
                    tax_per = tax_info.get('@percentOfOverall')

                    sub_tax = tax_info.get('sov:Subtaxonomy')
                    for sub_tax_info in sub_tax:
                        sub_tax_per = sub_tax_info.get('@percentOfOverall')
                        sub_tax_name = sub_tax_info.get('@name')

                        skill = sub_tax_info.get("sov:Skill")

                        if (skill != None):
                            for skill_info in skill:
                                skill_name = skill_info.get('@name', '')
                                skill_exists = skill_info.get('@existsInText', '')
                                if skill_exists == 'true':
                                    skill_months = skill_info.get('@totalMonths', '')
                                    skill_last_used = skill_info.get('@lastUsed', '')
                                else:
                                    skill_months = skill_info.get('@childrenTotalMonths', '')
                                    skill_last_used = skill_info.get('@childrenLastUsed', '')

                                result = {}
                                if tax_name:
                                    result['Taxonomy'] = tax_name
                                if tax_per:
                                    result['Taxonomy Percent'] = tax_per
                                if sub_tax_name:
                                    result['Sub Taxonomy'] = sub_tax_name
                                if sub_tax_per:
                                    result['Sub Taxonomy Per'] = sub_tax_per
                                if skill_name:
                                    result['Skill'] = skill_name
                                    if skill_months:
                                        result['Total Months'] = skill_months
                                    if skill_last_used:
                                        result['Last Used'] = skill_last_used

                                skill_details.append(result)

        return skill_details


def get_candidate_location(data, job_location):
    """
    Get candidate location
    :param data:
    :param job_location:
    :return:
    """
    candidate_location = []

    contact_info = data.get("ContactInfo", {})
    contact_method = ''
    if contact_info:
        contact_method = contact_info.get("ContactMethod", [])

    addr = ''
    if contact_method:
        for contact in contact_method:
            municipality = ''
            region = ''
            country_code = ''
            post_add = contact.get('PostalAddress', {})

            if post_add:
                country_code = post_add.get('CountryCode', '')
                postal_code = post_add.get('PostalCode', '')

                region = post_add.get('Region', [])
                if len(region) > 0:
                    region = region[0]
                municipality = post_add.get('Municipality', '')

                addr = municipality + " " + postal_code + " " + \
                       region + " " + country_code

                if addr and job_location:
                    distance_to_work = get_distance(job_location, addr)
                    print("Distance to Work", distance_to_work)

                result = {}
                if country_code:
                    result['Country Code'] = country_code
                if postal_code:
                    result['Postal Code'] = postal_code
                if region:
                    result['Region'] = region
                if municipality:
                    result['Municipality'] = municipality
                if distance_to_work:
                    result['Distance to Work'] = distance_to_work

                candidate_location.append(result)

    return candidate_location


def get_addr_from_postal_addr(element):
    """
    Format postal address
    :param element:
    :return:
    """
    addr = ''
    postal_adress = element["PostalAddress"]
    addr = postal_adress.get("Municipality", "") + " " + \
           postal_adress.get("PostalCode", "") + " " + \
           postal_adress.get("Region")[0] + " " + \
           postal_adress.get("CountryCode", "")

    return addr


def get_detail_parsed_information(data):
    """
        Detail parsed information
        :param data: Dict
        :return:
        """
    skills_result = {}
    data2 = data.get("UserArea")
    tax_root = ''
    user_area = data2.get("sov:ResumeUserArea")
    if user_area:
        exp_summary = user_area.get("sov:ExperienceSummary")
        if exp_summary:
            skill_taxonomy = exp_summary.get("sov:SkillsTaxonomyOutput")
            if skill_taxonomy:
                tax_root = skill_taxonomy.get("sov:TaxonomyRoot")

    for index, element in enumerate(tax_root):
        if element.get("sov:Taxonomy"):
            taxonomy = element.get("sov:Taxonomy")
            if taxonomy:
                tax_cnt = len(taxonomy)
                for i, tax in enumerate(taxonomy):
                    tax_var = "Taxonomy_" + str(i)
                    skills_result.update({
                        tax_var: {
                            "Name": tax.get("@name", "")
                        }
                    })
                    sub_tax = tax.get("sov:Subtaxonomy")
                    if sub_tax:
                        sub_tax_cnt = len(sub_tax)
                        for j, stax in enumerate(sub_tax):
                            sub_tax_var = "SubTaxonomy_" + str(j)
                            skills_result[tax_var].update({
                                sub_tax_var: {
                                    "Name": stax.get("@name", "")
                                }
                            })
                            skills = stax.get("sov:Skill")
                            if skills:
                                skills_cnt = len(skills)
                                for sk, skill in enumerate(skills):
                                    skill_var = "Skill_" + str(sk)
                                    skill_exists = skill.get('@existsInText', '')
                                    skills_result[tax_var][sub_tax_var].update({
                                        skill_var: {
                                            "Name": skill.get("@name", ""),
                                            "TotalMonths": skill.get("@totalMonths", "") \
                                                if skill_exists else None,
                                            "LastUsed": skill.get("@lastUsed", "") \
                                                if skill_exists else None
                                        }
                                    })
                                skills_result[tax_var][sub_tax_var].update({
                                    "SkillCnt": skills_cnt
                                })
                        skills_result[tax_var].update({
                            "SubTaxCnt": sub_tax_cnt
                        })
                skills_result.update({
                    "TaxCnt": tax_cnt
                })

    return skills_result


def get_distance(job_location, candidate_location):
    """
    Get the Job and Candidate Location
    """
    url = common_url_settings.get("LOCATION_API")
    payload = {"location_one": job_location, "location_two": candidate_location}
    headers = {
        'Content-Type': 'application/json'
    }
    distance = ''
    final_distance = ''

    try:

        response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
        data = response.text.encode('utf8')

        data1 = json.loads(data)
        distance = data1["data"]["distance"]
        measurement_unit = data1["data"]["measurement_unit"]
        final_distance = str(round(distance, 2)) + " " + measurement_unit

    except Exception as e:
        print("error in get_distance  ->  ", e)

    return final_distance


def get_job_details(job_id):
    """
    Get job details from Job Board
    :param job_id: String
    :return: array|string
    """
    headers = {
        'Authorization': common_url_settings. \
            get('JOB_BOARD_AUTHORIZATION')
    }
    response = requests.request("POST", common_url_settings. \
                                get('JOB_BOARD_JOB_DETAILS_URL'),
                                data={'job_reference_number': job_id},
                                headers=headers)

    try:
        response_info = json.loads(json.dumps(response.json()))

        # Set values in database before sending response here

        return response_info
    except ValueError:
        extracted_data = {
            'code': response.status_code,
            'message': 'Failed'
        }
        return extracted_data


def search_resume_in_internal_buckets(resume_id):
    """
    Search resume in internal buckets
    :param resume_id:
    :return:
    """
    internal_bucket_one = common_url_settings. \
        get("RESUME_MAIN_INDEX")
    internal_bucket_two = common_url_settings. \
        get("INTERNAL_BUCKET")
    if resume_id:
        resume_exists_on_bucket_one = \
            get_sovren_document_on_index_and_doc_id(
                internal_bucket_one,
                resume_id)
        if resume_exists_on_bucket_one:
            resume = resume_exists_on_bucket_one
        else:
            resume_exists_on_bucket_two = \
                get_sovren_document_on_index_and_doc_id(
                    internal_bucket_two,
                    resume_id)
            resume = resume_exists_on_bucket_two
        if resume:
            save_searched_resume_contact(resume_id, resume)
            return resume
        else:
            return None
    else:
        return None


def save_searched_resume_contact(resume_id, data):
    """
    Save searched resume contact
    :param resume_id:
    :param data:
    :return:
    """
    resume_text = json.loads(data["value"])
    parsed_resume = resume_text["Resume"]
    filtered_data = parsed_resume.get("StructuredXMLResume")
    contact_info = filtered_data.get("ContactInfo", {})
    if bool(contact_info):
        contact_payload = {
            "resume_id": resume_id,
            "ContactInfo": contact_info
        }
        CntFrmTpSchema.add(resume_id, contact_info)
        return True
    else:
        return False


def get_sovren_document_on_index_and_doc_id(resume_bucket, resume_id):
    """
    Get sovren document on bucket id and document index id
    :param resume_bucket:
    :param resume_id:
    :return:
    """
    headers = {
        'accept': "application/json",
        'sovren-accountid': sovren_url_settings. \
            get("SOVREN_ACCOUNT_ID"),
        'sovren-servicekey': sovren_url_settings. \
            get("SOVREN_ACCOUNT_SERVICE_KEY"),
    }
    request_url = sovren_url_settings. \
                      get("SOVREN_CREATE_INDEX_URL") + \
                  resume_bucket + '/documents/' + resume_id
    response = requests.request("GET", request_url, headers=headers)
    if response.status_code == HTTP_200_OK:
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


def duplicate_resume_error() -> dict:
    """
    Duplicate resume error message
    :return:
    """
    return {
        "code": HTTP_409_CONFLICT,
        "message": "Duplicate Resume",
        "value": None
    }


def index_document(request, parsed_document: str,
                   index_id: str, resume_id: str, res_doc_id: str) -> dict:
    """
    Index Document
    :param resume_id: String
    :param parsed_document: String
    :param index_id: String
    :param res_doc_id: String
    :return:
    """
    index_data = json.loads(parsed_document)
    index_data = index_data.get('Value', {}).get('ParsedDocument', '')

    payload = {
        "ParsedDocument": index_data,
    }
    calling_api = sovren_url_settings.get("SOVREN_CREATE_INDEX_URL") + index_id + '/documents/' + resume_id

    return connect_to_index_document_api(request, get_sovren_headers(), payload,
                                              calling_api)


def connect_to_index_document_api(request, header: dict, payload: dict,
                                  calling_api: str) -> dict:
    """
    Connect to Sovren API to Index Document
    :param header: Dictionary
    :param payload: Dictionary
    :param calling_api: String
    :return:
    """
    result = {}
    try:
        response = requests.request("POST", headers=header, \
                                    data=json.dumps(payload), url=calling_api)

        if response.status_code == HTTP_200_OK:
            response_info = json.loads(json.dumps(response.json()))
            request.app.logger.info("Successfully add a document to a Client Index ")
            result = {"code": response.status_code, \
                      'message': response_info['Info']['Message'], \
                      "data": response_info['Value']}
        else:
            result = {"code": response.status_code, \
                      "message": response.reason, \
                      "error": "Sovren unable to add a document to a Client Index "}
            request.app.logger.info("Sovren unable to add a document to a Client Index  ")
        return result

    except Exception as ex:
        request.app.logger.info("Error while adding a document to a Client Index  %s " % str(ex))
        result.update({
            "code": HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Error while adding a document to a Client Index from Sovren ",
            "error": "Exception is :" + str(ex)
        })
        return result

def call_sovren_parse_resume( request, base_64_encoded_string: str, revision_date: datetime,
                             index_id: str, resume_document_id: str,
                             resume_id: str, client_id: str, md5_hash: str) -> dict:
    """
    Parse resume
    :param resume_id: String
    :param base_64_encoded_string: String
    :param revision_date: Date
    :param index_id: String
    :param resume_document_id: String
    :return:
    """
    prs_resume = PrsResInfSchema()
    payload = {
        "DocumentAsBase64String": base_64_encoded_string,

        "IndexingOptions": {
            "IndexId": index_id,
            "DocumentId": resume_id,
        },
        "RevisionDate": revision_date,
    }
    calling_api = sovren_url_settings.get("SOVREN_PARSE_RESUME_URL")
    result = connect_to_sov_parse_resume_api(request, get_sovren_headers(), payload, \
                                 calling_api)
    if result.get("code") != HTTP_200_OK:
        return result

    # Save response to DB

    if result.get("code") == HTTP_200_OK:
        data_to_save = prs_resume.add(request, index_id, str(resume_document_id), resume_id, \
                                      json.dumps(result.get('data')), client_id, md5_hash, base_64_encoded_string)
        if data_to_save:
            request.app.logger.info("Parsed resume Saved in DB ")
            result.update({
                "saved_in_DB": True
            })
        else:
            request.app.logger.info("Parsed resume NOT Saved in DB ")
            result.update({
                "saved_in_DB": False
            })
        return result

def connect_to_sov_parse_resume_api( request, header: dict, payload: dict,
                   calling_api: str) -> dict:
    """
    Connect to Sovren API to parse job
    :param resume_id: String
    :param resume_document_id: String
    :param index_id: String
    :param header: Dictionary
    :param payload: Dictionary
    :param calling_api: String
    :return:
    """
    result = {}
    try:
        response = requests.request("POST", headers=header, \
                                    data=json.dumps(payload), url=calling_api)

        if response.status_code == HTTP_200_OK:
            response_info = json.loads(json.dumps(response.json()))
            request.app.logger.info("Successfully parsed the resume ")
            result = {"code": response.status_code, \
                      'message': response_info['Info']['Message'], \
                      "data": response_info['Value']['ParsedDocument']}
        else:
            result = {"code": response.status_code, \
                      "message": response.reason, \
                      "error": "Sovren unable to process the request"}
            request.app.logger.info("Sovren unable to proces the Resume request ")
        return result

    except Exception as ex:
        request.app.logger.info("Error while parsing Resume from Sovren %s " % str(ex))
        result.update({
            "code": HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Error while parsing Resume from Sovren ",
            "error": "Exception is :" + str(ex)
        })
        return result


def format_result_for_profile(request,resume_parsed):

    result = {}
    parsed_resume = resume_parsed.get("Resume",{})
    if parsed_resume:

        structure = parsed_resume.get('StructuredXMLResume', {})

        objective_data = get_formatted_objective(request, structure)

        per_data = get_formatted_personal_details(request,structure)

        exp_data = get_formatted_parsed_experience(request,structure)

        educ_data = get_formatted_parsed_education(request,structure)

        all_skills = get_formatted_all_skills(request,parsed_resume)

        result.update({
                "Summary": objective_data,
                "Personal_Details": per_data,
                "Experience": exp_data,
                "EducationDetail": educ_data,
                "Skills": all_skills
        })

    return result


def get_formatted_objective(request,parsed_data):

    object_data = parsed_data.get('Objective', '')
    return object_data


def get_formatted_personal_details(request,parsed_data):

    contact_info = parsed_data.get('ContactInfo', {})
    person = contact_info.get('PersonName', {})
    contact_method = contact_info.get('ContactMethod', [])
    city = ''
    country = ''
    region = ''
    lat = ''
    lon = ''
    contact_no = ''
    municipality = ''
    social_link = ''
    email = ''
    address = ''

    name = person.get('FormattedName', '')
    request.app.logger.info("Contact Info length is %s " % str(len(contact_method)))
    result = {}
    if len(contact_method) > 0:
        for val in contact_method:
            postal_addr = val.get('PostalAddress', {})
            request.app.logger.info("Postal Address is %s " % postal_addr)
            if postal_addr:
                country = postal_addr.get('CountryCode','')
                region_val = postal_addr.get('Region', [])
                if len(region_val) > 0:
                    region = region_val[0]
                municipality = postal_addr.get('Municipality', '')
                delivery_addr = postal_addr.get('DeliveryAddress', {})
                addr_val = delivery_addr.get('AddressLine', [])
                request.app.logger.info("Address is %s " % str(len(addr_val)))
                if len(addr_val) > 0:
                    address = addr_val[0]

            contact_no_val = val.get('Telephone', {})
            if contact_no_val:
                contact_no = contact_no_val.get('FormattedNumber', '')
            email = val.get('InternetEmailAddress', '')
            social_link = val.get('InternetWebAddress', '')

            result["candidate_name"] = name
            result["email"] = email
            result["contact_no"] = contact_no
            result["social_link"] = social_link
            result["address"] = address
            result["city"] = city
            result["country"] = country
            result["region"] = region
            result["municipality"] = municipality
            result["lat"] = lat
            result["lon"] = lon

    return result


def get_formatted_parsed_education(request,parsed_data):

    """
    Get parsed education information
    :param data:
    :return:
    """
    edu_details = []

    edu_hist = parsed_data.get("EducationHistory", {})
    if edu_hist:
        school_info = edu_hist.get("SchoolOrInstitution", [])

        for edu_info in school_info:
            university = ''
            degree = ''
            year = ''
            gpa = ''
            start_date = ''
            end_date = ''
            institution = ''
            degName = ''
            degDate = ''

            school = edu_info.get('School', '')

            for val in school:
                get_institution = val.get('SchoolName', '')
                if get_institution:
                    institution = get_institution

            degree = edu_info.get('Degree', '')
            for key in degree:
                get_degName = key.get('DegreeName', '')
                if get_degName:
                    degName = get_degName

                degree_major = key.get('DegreeMajor', '')

                for deg in degree_major:
                    deg_major_name = deg.get('Name', '')
                    if deg_major_name:
                        deg_major_val = deg_major_name[0]

                deg_date = key.get('DegreeDate', {})
                if deg_date:
                    degDate = deg_date.get('YearMonth', deg_date.get('Year', {}))

            result = {}

            result["university"] = institution
            result["degree"] = degName
            result["year"] = degDate
            result["start_date"] = start_date
            result["end_date"] = end_date
            result["gpa"] = gpa

            edu_details.append(result)
    return edu_details


def get_formatted_parsed_experience(request,parsed_data):
    """
    Get experience of the candidate
    :param data:
    :return:
    """
    exp_details = []

    emp_hist = parsed_data.get("EmploymentHistory", {})
    if emp_hist:
        emp_org_info = emp_hist.get("EmployerOrg", [])

        request.app.logger.info("EmployerORg length is %s " % str(len(emp_org_info)))
        for org_info in emp_org_info:
            title = ''
            start_date = ''
            end_date = ''
            description = ''
            org_name = ''
            org_name = org_info.get('EmployerOrgName', '')
            position_history = org_info.get("PositionHistory", [])

            #request.app.logger.info("PositionHistory length is %s " % str(len(position_history)))
            for key in position_history:
                get_title = key.get('Title', '')
                description = key.get('Description', '')

                if get_title:
                    title = get_title
                    #request.app.logger.info("Job Title is  %s " % title)
                get_postion_type = key.get('@positionType', '')
                if get_postion_type:
                    position_type = get_postion_type
                get_start_date = key.get('StartDate', '').get('YearMonth',
                                                              key.get('StartDate', '').get('AnyDate', ''))
                if get_start_date:
                    start_date = get_start_date
                get_end_date = key.get('EndDate', '').get('YearMonth', key.get('EndDate', '').get('StringDate', '')) \
                    if key.get('EndDate') else None
                if get_end_date:
                    end_date = get_end_date

            result = {}
            result["title"] = title
            result["organization"] = org_name
            result["start_date"] = start_date
            result["end_date"] = end_date
            result["description"] = description

            exp_details.append(result)

    return exp_details


def get_formatted_all_skills(request,parsed_data):
    """
    Get all skills
    :param data:
    :return:
    """
    all_skills = set()
    taxroot = ''
    data2 = parsed_data.get("UserArea", {})
    user_area = data2.get("sov:ResumeUserArea", {})
    if user_area:
        exp_summary = user_area.get("sov:ExperienceSummary")
        if exp_summary:
            skill_taxonomy = exp_summary.get("sov:SkillsTaxonomyOutput", {})
            if skill_taxonomy:
                taxroot = skill_taxonomy.get("sov:TaxonomyRoot", [])

            if taxroot:
                for tax in taxroot:
                    taxonomy = tax.get('sov:Taxonomy', [])
                    if taxonomy:
                        for tax_info in taxonomy:
                            sub_tax = tax_info.get('sov:Subtaxonomy', [])

                            for sub_tax_info in sub_tax:
                                skill = sub_tax_info.get("sov:Skill", [])

                                if skill != None:
                                    for skill_info in skill:
                                        skill_name = skill_info.get('@name', '')
                                        last_used = skill_info.get('@lastUsed')
                                        tot_months = skill_info.get('@totalMonths')

                                        result = {}
                                        if skill_name and (last_used and tot_months):
                                            result = skill_name

                                            all_skills.add(result)

    return list(all_skills)
