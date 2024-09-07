import json

from datetime import timedelta

import pytest
from freezegun import freeze_time

from utils.betslip_utils import get_past_date_formatted, filter_betslips_by_timestamp, calculate_avg_unit_size, \
    calculate_roi, get_decimal_from_odds
from utils.path_anchor import PROJECT_ROOT


@pytest.fixture
def mock_bets():
    mock_bets_path = str(PROJECT_ROOT) + "/tests/mock/mock_bets.json"
    with open(mock_bets_path, "r") as file:
        mock_bets = json.load(file)
    return mock_bets


@freeze_time("2024-01-08")
def test_get_past_date_formatted():
    delta = timedelta(weeks=1)
    expected = "2024-01-01"
    actual = get_past_date_formatted(delta)
    assert actual == expected


@freeze_time("2024-01-08")
def test_filter_betslips_by_timestamp(mock_bets):
    expected = mock_bets[2:]
    actual = filter_betslips_by_timestamp(mock_bets, timedelta(weeks=1))
    assert actual == expected


def test_calculate_avg_unit_size(mock_bets):
    expected = 50.0
    actual = calculate_avg_unit_size(mock_bets)
    assert actual == expected


def test_calculate_roi(mock_bets):
    expected = 25.39
    actual = calculate_roi(mock_bets)
    assert actual == expected


def test_get_decimal_from_odds():
    odds_neg = -110
    odds_pos = 250
    expected_neg = 1.91
    expected_pos = 3.5
    actual_neg = get_decimal_from_odds(odds_neg)
    actual_pos = get_decimal_from_odds(odds_pos)
    assert actual_neg == expected_neg
    assert actual_pos == expected_pos
