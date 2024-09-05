# coding=utf-8
"""
Copyright © 2020 U.S. TECH SOLUTIONS LICENSE

@version 0.2.0
Base test case
@author <rchakraborty@simplifyvms.com>
"""
import pytest
from starlette.testclient import TestClient
from src.routes.main import app


@pytest.fixture(scope="class")
def test_app():
    client = TestClient(app)
    yield client  # testing happens here
