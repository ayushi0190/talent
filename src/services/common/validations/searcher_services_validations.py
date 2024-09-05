# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Searcher services validations
@author <rchakraborty@simplifyvms.com>
@author <sreddy@simplifyvms.com>
@author <satya@simplifyvms.com>
"""
from typing import Optional, List
from pydantic import BaseModel, validator
from datetime import date


class DateRangeValidations(BaseModel):
    """ Date range validations """
    Minimum: Optional[date] = None
    Maximum: Optional[date] = None

    @validator("Minimum")
    def Minimum_must_be_string(cls, Minimum):
        """
        Custom validation message for Minimum
        :param Minimum:
        :return:
        """
        if not isinstance(Minimum, date):
            raise ValueError("Must be of date type")
        return Minimum

    @validator("Maximum")
    def Maximum_must_be_string(cls, Maximum):
        """
        Custom validation message for Maximum
        :param Maximum:
        :return:
        """
        if not isinstance(Maximum, date):
            raise ValueError("Must be of date type")
        return Maximum


class MonthRangeValidations(BaseModel):
    """ Month range validations """
    Minimum: Optional[int] = None
    Maximum: Optional[int] = None

    @validator("Minimum")
    def Minimum_must_be_int(cls, Minimum):
        """
        Custom validation message for Minimum
        :param Minimum:
        :return:
        """
        if not isinstance(Minimum, int):
            raise ValueError("Must be of integer type")
        return Minimum

    @validator("Maximum")
    def Maximum_must_be_int(cls, Maximum):
        """
        Custom validation message for Maximum
        :param Maximum:
        :return:
        """
        if not isinstance(Maximum, int):
            raise ValueError("Must be of integer type")
        return Maximum


class EducationValidations(BaseModel):
    """ Education validations """
    SchoolName: Optional[str] = None
    DegreeMajor: Optional[str] = None
    DegreeName: Optional[str] = None
    DegreeType: Optional[str] = None
    MinimumGPA: Optional[int] = 0

    @validator("SchoolName")
    def SchoolName_must_be_str(cls, SchoolName):
        """
        Custom validation message for SchoolName
        :param SchoolName:
        :return:
        """
        if not isinstance(SchoolName, str):
            raise ValueError("Must be of string type")
        return SchoolName

    @validator("DegreeMajor")
    def DegreeMajor_must_be_str(cls, DegreeMajor):
        """
        Custom validation message for Maximum
        :param DegreeMajor:
        :return:
        """
        if not isinstance(DegreeMajor, str):
            raise ValueError("Must be of string type")
        return DegreeMajor

    @validator("DegreeName")
    def DegreeName_must_be_str(cls, DegreeName):
        """
        Custom validation message for Maximum
        :param DegreeName:
        :return:
        """
        if not isinstance(DegreeName, str):
            raise ValueError("Must be of string type")
        return DegreeName

    @validator("DegreeType")
    def DegreeType_must_be_str(cls, DegreeType):
        """
        Custom validation message for Maximum
        :param DegreeType:
        :return:
        """
        if not isinstance(DegreeType, str):
            raise ValueError("Must be of string type")
        return DegreeType

    @validator("MinimumGPA")
    def MinimumGPA_must_be_int(cls, MinimumGPA):
        """
        Custom validation message for Maximum
        :param MinimumGPA:
        :return:
        """
        if not isinstance(MinimumGPA, int):
            raise ValueError("Must be of int type")
        return MinimumGPA


class GeoPointValidations(BaseModel):
    """ GeoPoint validations """
    Latitude: Optional[float] = 0.0
    Longitude: Optional[float] = 0.0

    @validator("Latitude")
    def Latitude_must_be_float(cls, Latitude):
        """
        Custom validation message for Latitude
        :param Latitude:
        :return:
        """
        if not isinstance(Latitude, float):
            raise ValueError("Must be of float type")
        return Latitude

    @validator("Longitude")
    def Longitude_must_be_float(cls, Longitude):
        """
        Custom validation message for Latitude
        :param Longitude:
        :return:
        """
        if not isinstance(Longitude, float):
            raise ValueError("Must be of float type")
        return Longitude


class LocationValidations(BaseModel):
    """ Location validations """
    CountryCode: Optional[str] = None
    Region: Optional[str] = None
    Municipality: Optional[str] = None
    PostalCode: Optional[str] = None
    Geopoint: Optional[GeoPointValidations] = None

    @validator("CountryCode")
    def CountryCode_must_be_str(cls, CountryCode):
        """
        Custom validation message for CountryCode
        :param CountryCode:
        :return:
        """
        if not isinstance(CountryCode, str):
            raise ValueError("Must be of string type")
        return CountryCode

    @validator("Region")
    def Region_must_be_str(cls, Region):
        """
        Custom validation message for Region
        :param Region:
        :return:
        """
        if not isinstance(Region, str):
            raise ValueError("Must be of string type")
        return Region

    @validator("Municipality")
    def Municipality_must_be_str(cls, Municipality):
        """
        Custom validation message for Municipality
        :param Municipality:
        :return:
        """
        if not isinstance(Municipality, str):
            raise ValueError("Must be of string type")
        return Municipality

    @validator("PostalCode")
    def PostalCode_must_be_str(cls, PostalCode):
        """
        Custom validation message for PostalCode
        :param PostalCode:
        :return:
        """
        if not isinstance(PostalCode, str):
            raise ValueError("Must be of string type")
        return PostalCode


class LocationCriteriaValidations(BaseModel):
    """ Location Criteria validations """
    Locations: Optional[List[LocationValidations]] = None
    Distance: Optional[int] = None
    DistanceUnit: Optional[str] = None
    GeocodeProvider: Optional[str] = None
    GeocodeProviderKey: Optional[str] = None

    @validator("Distance")
    def Distance_must_be_int(cls, Distance):
        """
        Custom validation message for Distance
        :param Distance:
        :return:
        """
        if not isinstance(Distance, int):
            raise ValueError("Must be of int type")
        return Distance

    @validator("DistanceUnit")
    def DistanceUnit_must_be_str(cls, DistanceUnit):
        """
        Custom validation message for DistanceUnit
        :param DistanceUnit:
        :return:
        """
        if not isinstance(DistanceUnit, str):
            raise ValueError("Must be of string type")
        return DistanceUnit

    @validator("GeocodeProvider")
    def GeocodeProvider_must_be_str(cls, GeocodeProvider):
        """
        Custom validation message for GeocodeProvider
        :param GeocodeProvider:
        :return:
        """
        if not isinstance(GeocodeProvider, str):
            raise ValueError("Must be of string type")
        return GeocodeProvider

    @validator("GeocodeProviderKey")
    def GeocodeProviderKey_must_be_str(cls, GeocodeProviderKey):
        """
        Custom validation message for GeocodeProviderKey
        :param GeocodeProviderKey:
        :return:
        """
        if not isinstance(GeocodeProviderKey, str):
            raise ValueError("Must be of string type")
        return GeocodeProviderKey


class SearcherServicesValidations(BaseModel):
    """ search services """
    resume_id: str

    @validator('resume_id')
    def resume_id_must_be_string(cls, resume_id):
        """
        Custom validation message for resume_id
        :param resume_id:
        :return:
        """
        if not isinstance(resume_id, str):
            raise ValueError('Must be of string type')
        if resume_id is None or len(resume_id) == 0:
            raise ValueError("Resume Id can not be null")
        return resume_id


class GetCandidateResumeValidations(BaseModel):
    """Search for Candidates Resume Validations"""
    resume_id: str

    @validator('resume_id')
    def resume_id_must_be_string(cls, resume_id):
        """
        Custom validation message for resume_id
        :param resume_id:
        :return:
        """
        if not isinstance(resume_id, str):
            raise ValueError('Must be of string type')
        if resume_id is None or len(resume_id) == 0:
            raise ValueError('Resume Id can not be null')
        return resume_id


class ParsedJobsValidations(BaseModel):
    """Search for Already Parsed Job Validations"""
    job_document_id: str

    @validator('job_document_id')
    def job_document_id_must_be_string(cls, job_document_id):
        """
        Custom validation message for job_document_id
        :param v:
        :return:
        """
        if not isinstance(job_document_id, str):
            raise ValueError('Must be of string type')
        if job_document_id is None or len(job_document_id) == 0:
            raise ValueError('Job Id can not be null')
        return job_document_id


class SearchJobsResumesValidations(BaseModel):
    """ Search for Job or Resumes Based on Criteria """
    Titles: List[str] = None
    Skills: List[str] = None
    bucket_source: Optional[List[str]]
    BucketType: str
    Location: Optional[str]
    BucketId: Optional[list]
    Count: Optional[int]
    AppliedJobs: Optional[list]
    SkillsMustAllExist: Optional[bool] = False
    Employers: Optional[List[str]] = None
    EmployersMustAllBeCurrentEmployer: Optional[bool] = False
    DateRange: Optional[DateRangeValidations] = None
    Educations: Optional[List[EducationValidations]] = None
    LocationCriteria: Optional[LocationCriteriaValidations] = None
    SearchExpression: Optional[str] = None
    SchoolNames: Optional[List[str]] = None
    DegreeNames: Optional[List[str]] = None
    DegreeTypes: Optional[List[str]] = None
    LanguagesKnown: Optional[List[str]] = None
    LanguagesKnownMustAllExist: Optional[bool] = False
    CurrentManagementLevel: Optional[str] = None
    DocumentLanguages: Optional[List[str]] = None
    MonthsExperience: Optional[MonthRangeValidations] = None
    MonthsManagementExperience: Optional[MonthRangeValidations] = None
    ExecutiveType: Optional[List[str]] = None
    Certifications: Optional[List[str]] = None

    @validator('Titles')
    def titles_must_be_list(cls, Titles):
        """
        Custom validation message for Titles
        :param v:
        :return:
        """
        if not isinstance(Titles, list):
            raise ValueError('Must be of list type')
        return Titles

    @validator('Skills')
    def skills_must_be_list(cls, Skills):
        """
        Custom validation message for Skills
        :param v:
        :return:
        """
        if not isinstance(Skills, list):
            raise ValueError('Must be of list type')
        return Skills

    @validator('BucketType')
    def bucket_type_must_be_str(cls, BucketType):
        """
        Custom validation message for BucketType
        :param v:
        :return:
        """
        if not isinstance(BucketType, str):
            raise ValueError('Must be of string type')
        if BucketType is None or len(BucketType) == 0:
            raise ValueError('Bucket Type can not be null')
        return BucketType

    @validator('Location')
    def location_must_be_str(cls, Location):
        """
        Custom validation message for Location
        :param v:
        :return:
        """
        if not isinstance(Location, str):
            raise ValueError('Must be of string type')
        if Location is None or len(Location) == 0:
            raise ValueError('Location can not be null')
        return Location

    @validator('BucketId')
    def bucket_id_must_be_list(cls, BucketId):
        """
        Custom validation message for BucketId
        :param v:
        :return:
        """
        if not isinstance(BucketId, list):
            raise ValueError('Must be of list type')
        return BucketId

    @validator('Count')
    def count_must_be_int(cls, Count):
        """
        Custom validation message for count
        :param v:
        :return:
        """
        if not isinstance(Count, int):
            raise ValueError('Must be of int type')
        return Count

    @validator('AppliedJobs')
    def applied_jobs_must_be_list(cls, AppliedJobs):
        """
        Custom validation message for applied_jobs
        :param v:
        :return:
        """
        if not isinstance(AppliedJobs, list):
            raise ValueError('Must be of list type')
        return AppliedJobs
