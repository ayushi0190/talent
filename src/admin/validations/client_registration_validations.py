
import pdb
from typing import List
from pydantic import BaseModel, validator
from datetime import date


class ParsingServiceToUseValidations(BaseModel):
    """ Parsing service to use validations """
    parse_job: bool
    parse_resume: bool

    @validator("parse_job")
    def parse_job_must_be_bool(cls, parse_job):
        """
        Custom validation message for parse_job
        :param parse_job:
        :return:
        """
        if not isinstance(parse_job, bool):
            raise ValueError("Must be of boolean type")
        return parse_job

    @validator("parse_resume")
    def parse_resume_must_be_bool(cls, parse_resume):
        """
        Custom validation message for parse_resume
        :param parse_resume:
        :return:
        """
        if not isinstance(parse_resume, bool):
            raise ValueError("Must be of boolean type")
        return parse_resume


class MatcherServiceToUseValidations(BaseModel):
    """ Matcher service to use validations """
    similar_jobs: bool
    discover_candidates: bool
    suggested_candidates: bool
    suggested_jobs: bool
    compare_candidates: bool

    @validator("similar_jobs")
    def similar_jobs_must_be_bool(cls, similar_jobs):
        """
        Custom validation message for similar_jobs
        :param similar_jobs:
        :return:
        """
        if not isinstance(similar_jobs, bool):
            raise ValueError("Must be of boolean type")
        return similar_jobs

    @validator("discover_candidates")
    def discover_candidates_must_be_bool(cls, discover_candidates):
        """
        Custom validation message for discover_candidates
        :param discover_candidates:
        :return:
        """
        if not isinstance(discover_candidates, bool):
            raise ValueError("Must be of boolean type")
        return discover_candidates

    @validator("suggested_candidates")
    def suggested_candidates_must_be_bool(cls, suggested_candidates):
        """
        Custom validation message for suggested_candidates
        :param suggested_candidates:
        :return:
        """
        if not isinstance(suggested_candidates, bool):
            raise ValueError("Must be of boolean type")
        return suggested_candidates

    @validator("suggested_jobs")
    def suggested_jobs_must_be_bool(cls, suggested_jobs):
        """
        Custom validation message for suggested_jobs
        :param suggested_jobs:
        :return:
        """
        if not isinstance(suggested_jobs, bool):
            raise ValueError("Must be of boolean type")
        return suggested_jobs

    @validator("compare_candidates")
    def compare_candidates_must_be_bool(cls, compare_candidates):
        """
        Custom validation message for compare_candidates
        :param compare_candidates:
        :return:
        """
        if not isinstance(compare_candidates, bool):
            raise ValueError("Must be of boolean type")
        return compare_candidates


class SearcherServiceToUseValidations(BaseModel):
    """ Searcher service to use validations """
    get_parsed_resume: bool
    get_parsed_job: bool
    search_jobs: bool

    @validator("get_parsed_resume")
    def get_parsed_resume_must_be_bool(cls, get_parsed_resume):
        """
        Custom validation message for get_parsed_resume
        :param get_parsed_resume:
        :return:
        """
        if not isinstance(get_parsed_resume, bool):
            raise ValueError("Must be of boolean type")
        return get_parsed_resume

    @validator("get_parsed_job")
    def get_parsed_job_must_be_bool(cls, get_parsed_job):
        """
        Custom validation message for get_parsed_job
        :param get_parsed_job:
        :return:
        """
        if not isinstance(get_parsed_job, bool):
            raise ValueError("Must be of boolean type")
        return get_parsed_job

    @validator("search_jobs")
    def search_jobs_must_be_bool(cls, search_jobs):
        """
        Custom validation message for search_jobs
        :param search_jobs:
        :return:
        """
        if not isinstance(search_jobs, bool):
            raise ValueError("Must be of boolean type")
        return search_jobs


class ScorerServiceToUseValidations(BaseModel):
    """ Searcher service to use validations """
    score_resume_job: bool = True

    @validator("score_resume_job")
    def score_resume_job_must_be_bool(cls, score_resume_job):
        """
        Custom validation message for score_resume_job
        :param score_resume_job:
        :return:
        """
        if not isinstance(score_resume_job, bool):
            raise ValueError("Must be of boolean type")
        return score_resume_job


class ServicesToUseValidations(BaseModel):
    """ Services to use validations """
    parsing: bool
    matching: bool
    searching: bool
    scoring: bool
    parser_service_to_use: ParsingServiceToUseValidations
    matcher_service_to_use: MatcherServiceToUseValidations
    searcher_services_to_use: SearcherServiceToUseValidations
    scorer_services_to_use: ScorerServiceToUseValidations

    @validator("parsing")
    def parsing_must_be_bool(cls, parsing):
        """
        Custom validation message for parsing
        :param parsing:
        :return:
        """
        if not isinstance(parsing, bool):
            raise ValueError("Must be of boolean type")
        return parsing

    @validator("matching")
    def matching_must_be_bool(cls, matching):
        """
        Custom validation message for matching
        :param matching:
        :return:
        """
        if not isinstance(matching, bool):
            raise ValueError("Must be of boolean type")
        return matching

    @validator("searching")
    def searching_must_be_bool(cls, searching):
        """
        Custom validation message for searcher
        :param searching:
        :return:
        """
        if not isinstance(searching, bool):
            raise ValueError("Must be of boolean type")
        return searching

    @validator("scoring")
    def scorer_must_be_bool(cls, scoring):
        """
        Custom validation message for scoring
        :param scoring:
        :return:
        """
        if not isinstance(scoring, bool):
            raise ValueError("Must be of boolean type")
        return scoring


class ToolToUseValidations(BaseModel):
    """ Pool to use validations """
    sovren: bool
    opening: bool
    simpai: bool

    @validator("sovren")
    def sovren_must_be_bool(cls, sovren):
        """
        Custom validation message for sovren
        :param sovren:
        :return:
        """
        if not isinstance(sovren, bool):
            raise ValueError("Must be of boolean type")
        return sovren

    @validator("opening")
    def opening_must_be_bool(cls, opening):
        """
        Custom validation message for opening
        :param opening:
        :return:
        """
        if not isinstance(opening, bool):
            raise ValueError("Must be of boolean type")
        return opening

    @validator("simpai")
    def simpai_must_be_bool(cls, simpai):
        """
        Custom validation message for simpai
        :param simpai:
        :return:
        """
        if not isinstance(simpai, bool):
            raise ValueError("Must be of boolean type")
        return simpai


class ClientRegistrationValidations(BaseModel):
    """ Client registration validations """
    company_name: str
    registration_date: date
    contract_period: int
    pol_shr: bool
    pol_prv: bool
    services_to_use: ServicesToUseValidations
    tool_to_use: ToolToUseValidations
    set_wgts: bool
    requested_for: str = "Create"

    @validator('company_name')
    def company_name_must_be_str(cls, company_name):
        """
        Custom validation message for company_name
        :param company_name:
        :return:
        """
        if not isinstance(company_name, str) or len(company_name) == 0:
            raise ValueError('Must be of string type')
        return company_name

    @validator('registration_date')
    def registration_date_must_be_date(cls, registration_date):
        """
        Custom validation message for Skills
        :param registration_date:
        :return:
        """
        if not isinstance(registration_date, date):
            raise ValueError('Must be of date type')
        if registration_date is None:
            raise ValueError('Registration date can not be null')
        return registration_date

    @validator('contract_period')
    def contract_period_must_be_int(cls, contract_period):
        """
        Custom validation message for contract_period
        :param contract_period:
        :return:
        """
        if not isinstance(contract_period, int):
            raise ValueError('Must be of integer type')
        return contract_period

    @validator('pol_shr')
    def pol_shr_must_be_bool(cls, pol_shr):
        """
        Custom validation message for pol_shr
        :param pol_shr:
        :return:
        """
        if not isinstance(pol_shr, bool):
            raise ValueError('Must be of boolean type')
        return pol_shr

    @validator('pol_prv')
    def pol_prv_must_be_bool(cls, pol_prv):
        """
        Custom validation message for pol_prv
        :param pol_prv:
        :return:
        """
        if not isinstance(pol_prv, bool):
            raise ValueError('Must be of boolean type')
        return pol_prv

    @validator('requested_for')
    def requested_for_must_be_str(cls, requested_for):
        """
        Custom validation message for requested_for
        :param requested_for:
        :return:
        """
        if not isinstance(requested_for, str):
            raise ValueError('Must be of string type')
        return requested_for
