import pytest
from unittest.mock import patch, MagicMock

from app.scripts.format_betslips import format_betslip


class TestFormatBetsLips:

    @patch("app.scripts.format_betslips.get_single_type_hedge_object")
    @patch("app.scripts.format_betslips.get_parlay_type_hedge_object")
    def test_format_betslip_no_type(self, mock_parlay_type, mock_single_type):
        mock_parlay_type.return_value = "parlay"
        mock_single_type.return_value = "single"
        betslip = {
            "bets": [],
        }
        with pytest.raises(TypeError) as exc_info:
            format_betslip(raw_betslip=betslip)
        assert str(exc_info.value) == "Betslip has no type attribute"

    @patch("app.scripts.format_betslips.get_single_type_hedge_object")
    @patch("app.scripts.format_betslips.get_parlay_type_hedge_object")
    def test_format_betslip_invalid_type(self, mock_parlay_type, mock_single_type):
        mock_parlay_type.return_value = "parlay"
        mock_single_type.return_value = "single"
        betslip = {
            "type": "waka",
            "bets": [],
        }
        with pytest.raises(TypeError) as exc_info:
            format_betslip(raw_betslip=betslip)
        assert str(exc_info.value) == "Betslip type waka not supported (only single and parlay allowed)"
