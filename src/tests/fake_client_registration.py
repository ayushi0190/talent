# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Fake client registration
@author <rchakraborty@simplifyvms.com>
"""
import json
from faker import Faker
from starlette.status import HTTP_400_BAD_REQUEST
from src.tests.base_case import test_app


class FakeClientRegistration:
    """
    Fake client registration
    """

    def register_client(self, test_app):
        """
        Register Client
        :param test_app:
        :return:
        """
        fake = Faker()
        try:
            data = json.dumps({
                "company_name": fake.company(),
                "registration_date": fake.date_between(start_date='-2m', end_date='today').strftime('%Y-%m-%d'),
                "contract_period": fake.pyint(),
                "pol_shr": True,
                "pol_prv": True,
                "services_to_use": {
                    "parsing": True,
                    "matching": True,
                    "searching": True,
                    "scoring": True,
                    "parser_service_to_use": {
                        "parse_job": True,
                        "parse_resume": True
                    },
                    "matcher_service_to_use": {
                        "similar_jobs": True,
                        "discover_candidates": True,
                        "suggested_candidates": True,
                        "suggested_jobs": True,
                        "compare_candidates": True
                    },
                    "searcher_services_to_use": {
                        "get_parsed_resume": True,
                        "get_parsed_job": True,
                        "search_jobs": True
                    },
                    "scorer_services_to_use": {
                        "score_resume_job": True
                    }
                },
                "tool_to_use": {
                    "sovren": True,
                    "opening": True,
                    "simpai": True
                }
            })
            response_register = test_app.post('/register/client', headers={"Content-Type": "application/json"},
                                              data=data)
            if response_register.status_code == 200:
                return response_register.json()
            else:
                return {
                    'code': HTTP_400_BAD_REQUEST,
                    'value': None
                }
        except Exception as es:
            pass


    def request_headers(self, client_id):
        """
        Create request headers
        :param client_id:
        :return:
        """
        return {
            "Content-Type": "application/json",
            "client_id": client_id
        }
