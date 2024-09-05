# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Graph services
@author <ankits@simplifyvms.com>
"""
import json
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_304_NOT_MODIFIED, HTTP_409_CONFLICT

from src.db.crud.sovren.prs_res_inf_schema import PrsResInfSchema
from src.services.common.helpers.ontology_properties import OntologyProperties

ontoprop = OntologyProperties()


class SovrenGraph:

    def __init__(self):
        self.count = 1
        self.result = {}
        self.error = []

    def listToString(self, s):
        """
        # initialize an empty string
        """
        str1 = ""
        # traverse in the string
        for ele in s:
            str1 = str1 + ele + ',' + '\n'

        return str1

    def get_graph(self, request, resume_id: str):
        graph_data = {}
        try:
            parse_resume_schema_obj = PrsResInfSchema()
            resume_parsed = parse_resume_schema_obj.get_graph_data(request, resume_id)

            if resume_parsed:
                request.app.logger.info("Type of Parsed Response for Graph Ontology%s " % type(resume_parsed.resp))
                resume_data = json.loads(resume_parsed.resp)
                resume_data = resume_data.get('Value', {}).get('ParsedDocument', '')
                resume_data = json.loads(resume_data)
                request.app.logger.info("Type of data pass to Ontology %s " % type(resume_data))

                graph_data = self.createOntology(request, resume_data)
                return graph_data

        except Exception as ex:
            request.app.logger.info("Error in get_graph function %s " % str(ex))
            graph_data.update({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error in get_graph function ",
                "error": "Exception is :" + str(ex)
            })
            return graph_data

    def createOntology(self,request, resume_details):

        self.result = {
            "_comment": "Empty ontology for WebVOWL Editor [Additional Information added by "
                        "WebVOWL Exporter Version: 1.1.7]",
            "header": {
                "languages": [
                    "en"
                ],
                "baseIris": [
                    "http://www.w3.org/2000/01/rdf-schema"
                ],

            },
            "namespace": [],
            "class": [],
            "classAttribute": [],
            "property": [],
            "propertyAttribute": []

        }

        if resume_details:
            resume_data = resume_details.get("Resume", {}).get("StructuredXMLResume", {})
            skill_data = resume_details.get("Resume", {}).get("UserArea", {})
            contact_info = resume_data.get('ContactInfo', {})

            self.get_personal_details(request, contact_info)
            self.get_experience(request, resume_data)
            self.get_education(request, resume_data)
            self.get_skills(request, skill_data)

            self.result["error"] = self.error

            return self.result

    def get_personal_details(self, request,parsed_contact):

        contact_no = ''
        email = ''
        social_link = ''
        country = ''
        region = ''
        municipality = ''
        address = ''
        candidate_name = 'No Name'

        try:
            if parsed_contact:

                person_name = parsed_contact.get('PersonName', {})
                if person_name:
                    candidate_name = person_name.get('FormattedName', 'No Name')

                request.app.logger.info("Candidate Name is %s " % candidate_name)
                contact_method = parsed_contact.get('ContactMethod', [])

                if len(contact_method) > 0:
                    for val in contact_method:
                        contact_no_val = val.get('Telephone', {})
                        if contact_no_val:
                            contact_no = contact_no_val.get('FormattedNumber', '')

                        email = val.get('InternetEmailAddress', '')
                        social_link = val.get('InternetWebAddress', '')

                        postal_addr = val.get('PostalAddress', {})
                        request.app.logger.info("Postal Address is %s " % postal_addr)
                        if postal_addr:
                            country = postal_addr.get('CountryCode', '')
                            region_val = postal_addr.get('Region', [])
                            if len(region_val) > 0:
                                region = region_val
                            municipality = postal_addr.get('Municipality', '')
                            delivery_addr = postal_addr.get('DeliveryAddress', {})
                            addr_val = delivery_addr.get('AddressLine', [])

                            request.app.logger.info("Address is %s " % str(len(addr_val)))
                            if len(addr_val) > 0:
                                address = addr_val[0]

                if contact_no or email or social_link or country or region or municipality or address:
                    self.result["class"].append(ontoprop.createClass("Class2", "owl:Class"))
                    self.result["classAttribute"].append(ontoprop.createclassAttribute("Class2", "Personal Details"))
                    self.result["property"].append(ontoprop.createProperty("objectProperty1", "owl:ObjectProperty"))
                    self.result["propertyAttribute"].append(
                        ontoprop.createpropertyAttribute("objectProperty1", "has_personal_details", "Class1",
                                                                  "Class2"))

                if contact_no:
                    request.app.logger.info("Contact No. is available %s" % contact_no)
                    self.result["class"].append(ontoprop.createClass("Data" + str(self.count), "rdfs:Datatype"))
                    self.result["classAttribute"].append(
                        ontoprop.createclassAttribute("Data" + str(self.count), contact_no, attr=True))
                    self.result["property"].append(
                        ontoprop.createProperty("datatypeProperty" + str(self.count), "owl:DatatypeProperty"))
                    self.result["propertyAttribute"].append(
                        ontoprop.createpropertyAttribute("datatypeProperty" + str(self.count), "has_phone", "Class2",
                                                                  "Data" + str(self.count)))
                    self.count += 1

                if email:
                    request.app.logger.info("Email is available %s" % email)
                    self.result["class"].append(ontoprop.createClass("Data" + str(self.count), "rdfs:Datatype"))
                    self.result["classAttribute"].append(
                        ontoprop.createclassAttribute("Data" + str(self.count), email, attr=True))
                    self.result["property"].append(
                        ontoprop.createProperty("datatypeProperty" + str(self.count), "owl:DatatypeProperty"))
                    self.result["propertyAttribute"].append(
                        ontoprop.createpropertyAttribute("datatypeProperty" + str(self.count), "has_email", "Class2",
                                                                  "Data" + str(self.count)))
                    self.count += 1

                if social_link:
                    request.app.logger.info("Social Link is available %s" % social_link)
                    self.result["class"].append(ontoprop.createClass("Data" + str(self.count), "rdfs:Datatype"))
                    self.result["classAttribute"].append(
                        ontoprop.createclassAttribute("Data" + str(self.count), social_link, attr=True))
                    self.result["property"].append(
                        ontoprop.createProperty("datatypeProperty" + str(self.count), "owl:DatatypeProperty"))
                    self.result["propertyAttribute"].append(
                        ontoprop.createpropertyAttribute("datatypeProperty" + str(self.count), "has_web_email",
                                                                  "Class2", "Data" + str(self.count)))
                    self.count += 1

                if region or country or municipality:
                    self.result["class"].append(ontoprop.createClass("Class3", "owl:Class"))
                    self.result["classAttribute"].append(ontoprop.createclassAttribute("Class3", "Address"))
                    self.result["property"].append(ontoprop.createProperty("objectProperty2", "owl:ObjectProperty"))
                    self.result["propertyAttribute"].append(
                        ontoprop.createpropertyAttribute("objectProperty2", "has_address", "Class2", "Class3"))

                if region:
                    request.app.logger.info("Region is available %s" % region)
                    self.result["class"].append(ontoprop.createClass("Data" + str(self.count), "rdfs:Datatype"))
                    self.result["classAttribute"].append(
                        ontoprop.createclassAttribute("Data" + str(self.count), region[0], attr=True))
                    self.result["property"].append(
                        ontoprop.createProperty("datatypeProperty" + str(self.count), "owl:DatatypeProperty"))
                    self.result["propertyAttribute"].append(
                        ontoprop.createpropertyAttribute("datatypeProperty" + str(self.count), "has_region", "Class3",
                                                                  "Data" + str(self.count)))
                    self.count += 1

                if country:
                    request.app.logger.info("country is available %s" % country)
                    self.result["class"].append(ontoprop.createClass("Data" + str(self.count), "rdfs:Datatype"))
                    self.result["classAttribute"].append(
                        ontoprop.createclassAttribute("Data" + str(self.count), country, attr=True))
                    self.result["property"].append(
                        ontoprop.createProperty("datatypeProperty" + str(self.count), "owl:DatatypeProperty"))
                    self.result["propertyAttribute"].append(
                        ontoprop.createpropertyAttribute("datatypeProperty" + str(self.count), "has_country", "Class3",
                                                                  "Data" + str(self.count)))
                    self.count += 1

                if municipality:
                    request.app.logger.info("municipality is available %s" % municipality)
                    self.result["class"].append(ontoprop.createClass("Data" + str(self.count), "rdfs:Datatype"))
                    self.result["classAttribute"].append(
                        ontoprop.createclassAttribute("Data" + str(self.count), municipality, attr=True))
                    self.result["property"].append(
                        ontoprop.createProperty("datatypeProperty" + str(self.count), "owl:DatatypeProperty"))
                    self.result["propertyAttribute"].append(
                        ontoprop.createpropertyAttribute("datatypeProperty" + str(self.count), "has_municipality",
                                                                  "Class3", "Data" + str(self.count)))
                    self.count += 1

                if address:
                    request.app.logger.info("address line is available %s" % address)
                    self.result["class"].append(ontoprop.createClass("Data" + str(self.count), "rdfs:Datatype"))
                    self.result["classAttribute"].append(
                        ontoprop.createclassAttribute("Data" + str(self.count), address, attr=True))
                    self.result["property"].append(
                        ontoprop.createProperty("datatypeProperty" + str(self.count), "owl:DatatypeProperty"))
                    self.result["propertyAttribute"].append(
                        ontoprop.createpropertyAttribute("datatypeProperty" + str(self.count), "has_address_line",
                                                         "Class3", "Data" + str(self.count)))
                    self.count += 1

            if candidate_name:
                self.result["class"].append(ontoprop.createClass("Class1", "owl:equivalentClass"))
                self.result["classAttribute"].append(ontoprop.createclassAttribute("Class1", candidate_name))

        except Exception as ex:
            request.app.logger.info("Error in Processing Personal Details while creating ontology from Sovren %s " % str(ex))
            self.error.append({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error in Processing Personal Details while creating ontology from Sovren ",
                "error": "Exception is :" + str(ex)
            })

    def get_experience(self, request,resume_details):

        try:

            employment_history = resume_details.get("EmploymentHistory", {})

            if employment_history:
                employee_org = employment_history.get("EmployerOrg", [])

                request.app.logger.info("Employee data is %s " % employee_org)
                request.app.logger.info("No. of Employee Orgns are %s " % str(len(employee_org)))
                if len(employee_org) > 0:

                    self.result["class"].append(ontoprop.createClass("Class5", "owl:Class"))
                    self.result["classAttribute"].append(ontoprop.createclassAttribute("Class5", "Experience"))
                    self.result["property"].append(ontoprop.createProperty("objectProperty4", "owl:ObjectProperty"))
                    self.result["propertyAttribute"].append(
                        ontoprop.createpropertyAttribute("objectProperty4", "has_work_history", "Class1", "Class5"))

                    for val in employee_org[:5]:

                        org_name = val.get('EmployerOrgName', '')

                        request.app.logger.info("EmployerOrgName is %s " % org_name)
                        position_history = val.get("PositionHistory", [])
                        title = ''
                        start_date = ''
                        end_date = ''
                        position_type = ''

                        for key in position_history:
                            get_title = key.get('Title', '')

                            request.app.logger.info("Title is %s " % get_title)
                            if get_title:
                                title = get_title
                            get_postion_type = key.get('@positionType', '')
                            if get_postion_type:
                                position_type = get_postion_type
                            get_start_date = key.get('StartDate', {}).get('YearMonth',
                                                                          key.get('StartDate', {}).get('AnyDate', ''))
                            if get_start_date:
                                start_date = get_start_date
                            get_end_date = key.get('EndDate', {}).get('YearMonth',
                                                                      key.get('EndDate', {}).get('StringDate', ''))
                            if get_end_date:
                                end_date = get_end_date

                        result = None
                        if org_name:
                            result = org_name + '           \t \t \n'
                            if title:
                                result += title + '\n'
                            if start_date:
                                result += start_date + '\n'
                            if end_date:
                                result += end_date + '\n'
                            if position_type:
                                result += position_type

                        if result:
                            self.result["class"].append(ontoprop.createClass("Data" + str(self.count), "rdfs:Datatype"))
                            self.result["classAttribute"].append(
                                ontoprop.createclassAttribute("Data" + str(self.count), result, attr=True))
                            self.result["property"].append(
                                ontoprop.createProperty("datatypeProperty" + str(self.count), "owl:DatatypeProperty"))
                            self.result["propertyAttribute"].append(
                                ontoprop.createpropertyAttribute("datatypeProperty" + str(self.count), "has_experience",
                                                                          "Class5", "Data" + str(self.count)))

                        self.count += 1

        except Exception as ex:
            request.app.logger.info(
                "Error in Processing Experience Section while creating ontology from Sovren %s " % str(ex))
            self.error.append({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error in Processing Experience Section while creating ontology from Sovren ",
                "error": "Exception is :" + str(ex)
            })

    def get_education(self, request,  resume_details):

        try:

            education = resume_details.get("EducationHistory", {})
            if education:
                school_data = education.get("SchoolOrInstitution", [])

                request.app.logger.info("No. of Institutions are %s " % str(len(school_data)))
                request.app.logger.info("Institutions are %s " % school_data)
                if len(school_data) > 0:
                    self.result["class"].append(ontoprop.createClass("Class4", "owl:Class"))
                    self.result["classAttribute"].append(ontoprop.createclassAttribute("Class4", "Education"))
                    self.result["property"].append(ontoprop.createProperty("objectProperty3", "owl:ObjectProperty"))
                    self.result["propertyAttribute"].append(
                        ontoprop.createpropertyAttribute("objectProperty3", "has_education", "Class1", "Class4"))

                    deg_major_val = ''
                    institution = ''
                    degName = ''
                    degDate = ''

                    for school_val in school_data[:5]:
                        school = school_val.get('School', [])
                        request.app.logger.info("school is %s " % school)

                        for val in school:
                            get_institution = val.get('SchoolName', '')

                            request.app.logger.info("SchoolName is %s " % get_institution)
                            if get_institution:
                                institution = get_institution
                        degree = school_val.get('Degree', [])
                        for key in degree:
                            get_degName = key.get('DegreeName', '')

                            request.app.logger.info("DegreeName is %s " % get_degName)
                            if get_degName:
                                degName = get_degName
                            degree_major = key.get('DegreeMajor', [])
                            for deg in degree_major:
                                deg_major_name = deg.get('Name', '')
                                if deg_major_name:
                                    deg_major_val = deg_major_name[0]
                            deg_date = key.get('DegreeDate', {})
                            if deg_date:
                                degDate = deg_date.get('YearMonth')

                        result = None
                        if degName or deg_major_val or degDate or institution:
                            if degName:
                                result = degName + '           \t \t \n'
                            else:
                                result = '                   \t  \t \t \t \n'
                            if deg_major_val:
                                result += deg_major_val + '\n'
                            if degDate:
                                result += degDate + '\n'
                            if institution:
                                result += institution

                        if result:
                            self.result["class"].append(ontoprop.createClass("Data" + str(self.count), "rdfs:Datatype"))
                            self.result["classAttribute"].append(
                                ontoprop.createclassAttribute("Data" + str(self.count), result, attr=True))
                            self.result["property"].append(
                                ontoprop.createProperty("datatypeProperty" + str(self.count), "owl:DatatypeProperty"))
                            self.result["propertyAttribute"].append(
                                ontoprop.createpropertyAttribute("datatypeProperty" + str(self.count), "has_degree",
                                                                          "Class4", "Data" + str(self.count)))
                        self.count += 1

        except Exception as ex:
            request.app.logger.info(
                "Error in Processing Education Section while creating ontology from Sovren %s " % str(ex))
            self.error.append({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error in Processing Education Section while creating ontology from Sovren ",
                "error": "Exception is :" + str(ex)
            })

    def get_skills(self, request, resume_details):

        try:

            taxroot = ''
            user_area = resume_details.get("sov:ResumeUserArea")
            if user_area:
                exp_summary = user_area.get("sov:ExperienceSummary" ,{})
                if exp_summary:
                    skill_taxonomy = exp_summary.get("sov:SkillsTaxonomyOutput",[])
                    if len(skill_taxonomy) > 0:
                        taxroot = skill_taxonomy.get("sov:TaxonomyRoot",[])

            skillCount = 200
            subtaxCount = 100
            taxCount = 7
            childskillcount = 500

            request.app.logger.info(" No. of TaxonomyRoot in Skills are %s " % str(len(taxroot)))
            if len(taxroot) > 0:
                for tax in taxroot:
                    taxonomy = tax.get('sov:Taxonomy', [])

                    request.app.logger.info(" No. of Taxonomy in Skills are %s " % str(len(taxroot)))
                    if len(taxonomy) > 0:
                        self.result["class"].append(ontoprop.createClass("Class6", "owl:Class"))
                        self.result["classAttribute"].append(ontoprop.createclassAttribute("Class6", "Skills"))
                        self.result["property"].append(ontoprop.createProperty("objectProperty5", "owl:ObjectProperty"))
                        self.result["propertyAttribute"].append(
                            ontoprop.createpropertyAttribute("objectProperty5", "has_skills_taxonomy", "Class1",
                                                                      "Class6"))

                        rootCount = 0
                        for tax_info in taxonomy:
                            tax_name = tax_info.get('@name', '')
                            tax_per = tax_info.get('@percentOfOverall')
                            rootCount += 1

                            if rootCount in [1, 2]:
                                self.result["class"].append(ontoprop.createClass("Class" + str(taxCount), "owl:Class"))
                                self.result["classAttribute"].append(
                                    ontoprop.createclassAttribute("Class" + str(taxCount), tax_name))
                                self.result["property"].append(ontoprop.createProperty("objectProperty" + str(taxCount),
                                                                                         "owl:ObjectProperty"))
                                self.result["propertyAttribute"].append(
                                    ontoprop.createpropertyAttribute("objectProperty" + str(taxCount),
                                                                              "has_taxonomy", "Class6",
                                                                              "Class" + str(taxCount)))

                                taxCount += 1
                                sub_tax = tax_info.get('sov:Subtaxonomy')
                                subrootCount = 0
                                for sub_tax_info in sub_tax:
                                    sub_tax_per = sub_tax_info.get('@percentOfOverall')
                                    sub_tax_name = sub_tax_info.get('@name')
                                    subrootCount += 1

                                    if subrootCount in [1, 2]:
                                        self.result["class"].append(
                                            ontoprop.createClass("Class" + str(subtaxCount), "owl:Class"))
                                        self.result["classAttribute"].append(
                                            ontoprop.createclassAttribute("Class" + str(subtaxCount),
                                                                                   sub_tax_name))
                                        self.result["property"].append(
                                            ontoprop.createProperty("objectProperty" + str(subtaxCount),
                                                                             "owl:ObjectProperty"))
                                        self.result["propertyAttribute"].append(
                                            ontoprop.createpropertyAttribute("objectProperty" + str(subtaxCount),
                                                                                      "has_sub_taxonomy",
                                                                                      "Class" + str(taxCount - 1),
                                                                                      "Class" + str(subtaxCount)))

                                        subtaxCount += 1
                                        skill = sub_tax_info.get("sov:Skill")
                                        if (skill != None):
                                            for skill_info in skill[:10]:
                                                skill_name = skill_info.get('@name', '')
                                                skill_exists = skill_info.get('@existsInText', '')
                                                if skill_exists == 'true':
                                                    skill_months = skill_info.get('@totalMonths', '')
                                                    skill_last_used = skill_info.get('@lastUsed', '')
                                                else:
                                                    skill_months = skill_info.get('@childrenTotalMonths', '')
                                                    skill_last_used = skill_info.get('@childrenLastUsed', '')

                                                result = None
                                                if skill_name:
                                                    result = "name: " + skill_name + '           \t \t \n'
                                                    if skill_months:
                                                        result += "totalMonths: " + skill_months + '\n'
                                                    if skill_last_used:
                                                        result += "lastUsed: " + skill_last_used + '\n'

                                                if result:
                                                    self.result["class"].append(
                                                        ontoprop.createClass("Data" + str(skillCount),
                                                                                      "rdfs:Datatype"))
                                                    self.result["classAttribute"].append(
                                                        ontoprop.createclassAttribute("Data" + str(skillCount),
                                                                                               result, attr=True))
                                                    self.result["property"].append(ontoprop.createProperty(
                                                        "datatypeProperty" + str(skillCount), "owl:DatatypeProperty"))
                                                    self.result["propertyAttribute"].append(
                                                        ontoprop.createpropertyAttribute(
                                                            "datatypeProperty" + str(skillCount), "has_skill",
                                                            "Class" + str(subtaxCount - 1), "Data" + str(skillCount)))

                                                    skillCount += 1

                                                child_skill = skill_info.get('sov:ChildSkill')
                                                if (child_skill != None):
                                                    for child_skill_info in child_skill[:5]:
                                                        child_skill_name = child_skill_info.get('@name')
                                                        child_skill_months = child_skill_info.get('@totalMonths', '')
                                                        child_skill_last_used = child_skill_info.get('@lastUsed', '')

                                                        result = None
                                                        if child_skill_name:
                                                            result = "name: " + child_skill_name + '           \t \t \n'
                                                            if child_skill_months:
                                                                result += "totalMonths: " + child_skill_months + '\n'
                                                            if child_skill_last_used:
                                                                result += "lastUsed: " + child_skill_last_used + '\n'

                                                        if result:
                                                            self.result["class"].append(
                                                                ontoprop.createClass("Data" + str(childskillcount),
                                                                                              "rdfs:Datatype"))
                                                            self.result["classAttribute"].append(
                                                                ontoprop.createclassAttribute(
                                                                    "Data" + str(childskillcount), result, attr=True))
                                                            self.result["property"].append(ontoprop.createProperty(
                                                                "datatypeProperty" + str(childskillcount),
                                                                "owl:DatatypeProperty"))
                                                            self.result["propertyAttribute"].append(
                                                                ontoprop.createpropertyAttribute(
                                                                    "datatypeProperty" + str(childskillcount),
                                                                    "has_sub_skill", "Data" + str(skillCount - 1),
                                                                    "Data" + str(childskillcount)))
                                                            childskillcount += 1

        except Exception as ex:
            request.app.logger.info(
                "Error in Processing Skill Section while creating ontology from Sovren %s " % str(ex))
            self.error.append({
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Error in Processing Skill Section while creating ontology from Sovren ",
                "error": "Exception is :" + str(ex)
            })

