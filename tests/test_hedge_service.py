from unittest.mock import patch

import pytest

from models.api.api_models import CreateAccountLinkRequest
from service.hedge_service import HedgeService
from service.sharp_sports_service import SharpSportsService


class TestHedgeService:

    mock_request_data = {
        "first": "nico",
        "last": "colosso",
        "phone": "123-456-7890",
        "book": "Fanduel",
        "state_abbr": "NY",
    }
    mock_request = CreateAccountLinkRequest(**mock_request_data)

    @pytest.fixture
    @patch("repository.mongo_repository.MongoRepository")
    @patch("service.sharp_sports_service.SharpSportsService")
    def hedge_service(self, mock_mongo_repository, mock_sharp_sports_service):
        return HedgeService()

    @patch.object(SharpSportsService, "create_extension_auth_token")
    @patch.object(SharpSportsService, "create_context")
    @patch.object(HedgeService, "create_user")
    def test_create_account_link(
        self, mock_create_user, mock_create_context, mock_create_token, hedge_service
    ):
        mock_create_user.return_value = "nico_colosso"
        mock_create_token.return_value = "abcd"
        mock_create_context.return_value = "1234"
        cid, url, exc_message = hedge_service.create_account_link(self.mock_request)
        assert cid == "1234"
        assert (
            url
            == "https://ui.sharpsports.io/link/1234/region/BRGN_ab5628fa79344c39bce8fec0f17fbdcc/login"
        )
        assert exc_message == ""

    @patch.object(SharpSportsService, "create_extension_auth_token")
    @patch.object(SharpSportsService, "create_context")
    @patch.object(HedgeService, "create_user")
    def test_create_account_link_no_sdk(
        self, mock_create_user, mock_create_context, mock_create_token, hedge_service
    ):
        mock_create_user.return_value = "nico_colosso"
        mock_create_token.return_value = "abcd"
        mock_create_context.return_value = "1234"
        request = self.mock_request
        request.book = "Fliff"
        cid, url, exc_message = hedge_service.create_account_link(request)
        assert cid == "1234"
        assert url == "https://ui.sharpsports.io/link/1234"
        assert exc_message == ""
