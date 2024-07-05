import json

from datetime import date, timedelta

import pytest
from freezegun import freeze_time

from utils.betslip_utils import *
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
    expected = 55.0
    actual = calculate_avg_unit_size(mock_bets)
    assert actual == expected
