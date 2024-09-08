"""
Test the API Handler
"""
import os

from base64 import b64encode
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from http import HTTPStatus
from pytest import fixture

from app.hedge import app

VERSION = "v1"
client = TestClient(app)

load_dotenv()
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")


class TestHedge:

    @fixture(scope="module")
    def valid_auth_header(self):
        return generate_basic_auth_token(username=MONGO_USER, password=MONGO_PASSWORD)

    def test_ping(self):
        route = f"{VERSION}/ping"
        response = client.get(route)
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"message": "Ping successful!"}

    def test_auth_success(self, valid_auth_header):
        route = f"{VERSION}/test-auth"
        response = client.get(route, headers={"Authorization": valid_auth_header})
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"message": "Successfully authenticated!"}

    def test_auth_no_creds(self):
        route = f"{VERSION}/test-auth"
        response = client.get(route)
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_auth_invalid_creds(self):
        route = f"{VERSION}/test-auth"
        invalid_auth_header = generate_basic_auth_token(username="bad_user", password="pwd")
        response = client.get(route, headers={"Authorization": invalid_auth_header})
        assert response.status_code == HTTPStatus.UNAUTHORIZED


def generate_basic_auth_token(username: str, password: str) -> str:
    token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"
