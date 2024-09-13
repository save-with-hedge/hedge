"""
Test the API Handler
"""
import os

from base64 import b64encode
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from http import HTTPStatus
from pytest import fixture
from unittest.mock import patch

from app.hedge import app
from app.repository.mongo_repository import MongoRepository

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

    @patch.object(MongoRepository, "is_admin")
    def test_auth_success(self, mock_is_admin):
        mock_is_admin.return_value = True
        route = f"{VERSION}/test-auth"
        auth_token = generate_basic_auth_token(username="user", password="pwd")
        response = client.get(route, headers={"Authorization": auth_token})
        assert response.status_code == HTTPStatus.OK
        assert response.json() == {"message": "Successfully authenticated!"}

    @patch.object(MongoRepository, "is_admin")
    def test_auth_failure(self, mock_is_admin):
        mock_is_admin.return_value = False
        route = f"{VERSION}/test-auth"
        auth_token = generate_basic_auth_token(username="user", password="pwd")
        response = client.get(route, headers={"Authorization": auth_token})
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_auth_no_creds(self):
        route = f"{VERSION}/test-auth"
        response = client.get(route)
        assert response.status_code == HTTPStatus.UNAUTHORIZED


def generate_basic_auth_token(username: str, password: str) -> str:
    token = b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
    return f"Basic {token}"
