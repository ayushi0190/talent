import requests
import pdb
from starlette.status import HTTP_400_BAD_REQUEST
from src.services.common.config.common_config import common_url_settings


class ListJobsForTest:
    """
    Get jobs for unit test
    """

    def get_job_sources(self):
        """
        Get job resources
        :return: int
        """
        response = requests.request("GET", headers=self.request_headers(), url=common_url_settings.get("LIST_JOBS_FROM_JOB_BOARD"))
        result_data = response.json()
        source_id = None
        if response.status_code == 200:
            if result_data.get("result"):
                for source in result_data.get("result"):
                    if source["source_name"] == common_url_settings.get("SOURCE_NAME_FOR_TEST_JOBS"):
                        source_id = source["id"]
            return {"source_id": source_id}
        else:
            return {
                'code': HTTP_400_BAD_REQUEST,
                'value': None
            }

    def get_job_ref_num(self, source_id):
        """
        Get job reference number
        :param source_id: int
        :return: dict
        """

        response = requests.request("POST", data={"source_id": source_id}, headers=self.request_headers(), url=common_url_settings.get("LIST_SOURCE_JOBS_FROM_JOB_BOARD"))
        test_jobs_list = []
        result_data = response.json()
        if response.status_code == 200:
            if result_data.get("result"):
                for job in result_data["result"]:
                    test_jobs_list.append(job["job_reference_number"])
            return {"jobs_list": test_jobs_list}
        else:
            return {
                'code': HTTP_400_BAD_REQUEST,
                'value': None
            }

    def request_headers(self):
        """
        Get request headers
        :return: dict
        """
        header = {
            "Content-Type": "application/json",
            "Authorization": common_url_settings.get("JOB_BOARD_AUTHORIZATION"),

        }
        return header