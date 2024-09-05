# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Miscellaneous helper methods
@author <ankits@simplifyvms.com>
"""





def format_result_for_profile(request,resume_parsed):

    result = {}
    if resume_parsed:

        objective_data = "" #get_formatted_objective(request, resume_parsed)

        per_data = get_formatted_personal_details(resume_parsed)

        exp_data = get_formatted_parsed_experience(resume_parsed)

        educ_data = get_formatted_parsed_education(resume_parsed)

        all_skills = get_formatted_all_skills(resume_parsed)

        result.update({
                "Summary": objective_data,
                "Personal_Details": per_data,
                "Experience": exp_data,
                "EducationDetail": educ_data,
                "Skills": all_skills
        })

    return result
'''
def format_result_for_profile(resume_parsed):

        result = {}
        parsed_data = resume_parsed.get('value',{})

        if parsed_data:
            logger.info("In If condition")
            raw_text = parsed_data.get('raw_text', '')

            per_data = CustomParserAPI.get_personal_details(parsed_data)
            logger.info("Get personal details %s" % per_data)

            educ_data = CustomParserAPI.get_parsed_education(parsed_data)

            exp_data = CustomParserAPI.get_parsed_experience(parsed_data)

            skills_data = CustomParserAPI.get_parsed_skill(parsed_data)

            result.update({
                'message': resume_parsed.get('message', ''),
                'code': resume_parsed.get('code', '200'),
                "value": {
                    "Personal_Details": per_data,
                    "Experience": exp_data,
                    "EducationDetail": educ_data,
                    "Skills": skills_data}
            })

        return result

'''

def get_formatted_personal_details(parsed_data):

        per_details = parsed_data.get('personal details',{})
        city = ''
        country = ''
        region = ''
        lat = ''
        lon = ''
        contact_no = ''
        add = ''
        state = ''
        name = per_details.get('candidate_name','')
        email = per_details.get('email','')
        contact_no_val = per_details.get('contact_no',[])
        if len(contact_no_val) > 0:
            contact_no = contact_no_val[0]
        social_link = per_details.get('socialLink','')
        try:
            address = per_details.get("address",{}).get("formatted_address",{})
        except:
            address = {}
        if address:
            add = address.get("address", "")
            city = address.get("city/district/county", "")
            state = address.get("state", "")
            country = address.get("country", "")

        result = {}
        result["candidate_name"] = name
        result["email"] = email
        result["contact_no"] = contact_no
        result["social_link"] = social_link
        result["address"] = add
        result["city"] = city
        result["country"] = country
        result["region"] = state
        result["lat"] = lat
        result["lon"] = lon

        return result

def get_formatted_parsed_education(parsed_data):
        educations = []
        university = ''
        degree = ''
        year = ''
        gpa = ''
        start_date = ''
        end_date = ''
        major = ''
        education_details = parsed_data.get('education', [])
        print("Education: ", len(education_details))
        if len(education_details) > 0:
            for value in education_details:
                university = value.get('univ','')
                degree = value.get('degree','')
                year = value.get('year','')
                gpa = value.get('gpa','')
                major = value.get('major', '')

                result = {}
                result["university"] = university
                result["degree"] = degree
                result["year"] = year
                result["start_date"] = start_date
                result["end_date"] = end_date
                result["gpa"] = gpa
                result["major"] = major

                educations.append(result)

        return educations

def get_formatted_parsed_experience(parsed_data):

        employments = []
        experience_details = parsed_data.get('experience', [])
        organization = ''
        start_date = ''
        end_date = ''
        description = ''
        role = ''

        if len(experience_details) > 0:
            for value in experience_details:
                organization_val = value.get('organization',[])
                if organization_val is not None:
                    if len(organization_val) > 0:
                        organization = organization_val[0]

                start_date = value.get('from','')
                end_date = value.get('to','')
                description = value.get('description','')
                role_val = value.get('role',[])
                if len(role_val) > 0:
                    role = role_val[0]

                result = {}
                result["title"] = role
                result["organization"] = organization
                result["start_date"] = start_date
                result["end_date"] = end_date
                result["description"] = description

                employments.append(result)

        return employments

def get_formatted_all_skills(parsed_data):
        skill_details = parsed_data.get('skills_cumulative_exp', [])
        # skill_info = []
        # for skills in skill_details:
        #     skill = skills.get('skills_name')

        #     result = {}
        #     result["skills"] = skill

        #     skill_info.append(skill)

        # return skill_info

        skill_info = list()
        for skill_exp in skill_details:
            skill_ind_details = skill_details.get(skill_exp, [])
            for skills in skill_ind_details:
                skill = skills.get('skills_name')
                result = dict()
                result['skills'] = skill

                skill_info.append(result)

        return skill_info


