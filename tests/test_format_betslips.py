from models.hedge_betslip import HedgeBetslip, Result
from scripts.format_betslips import format_betslip

mock_raw_betslip_single = {
    "book": {
        "id": "BOOK_1aac80eb006640bd9722eb25ae73845a",
        "name": "Underdog",
        "abbr": "ud",
    },
    "timePlaced": None,
    "type": "single",
    "oddsAmerican": 200,
    "atRisk": 1000,
    "outcome": "loss",
    "netProfit": -1000,
    "timeClosed": "2023-10-24T00:07:00Z",
    "bets": [
        {
            "type": "prop",
            "event": {
                "sport": "Baseball",
            },
            "bookDescription": "ARI @ PHI - Merrill Kelly Strikeouts O/U - lower 5.0",
        },
    ],
}

mock_raw_betslip_parlay = {
    "book": {"id": "BOOK_Rf7xRhS7TKQUl94Xkt5w", "name": "Fanduel", "abbr": "fd"},
    "timePlaced": "2024-04-26T00:49:26Z",
    "type": "parlay",
    "oddsAmerican": 1572,
    "atRisk": 12500,
    "outcome": "loss",
    "netProfit": -12500,
    "timeClosed": None,
    "dateClosed": "2024-04-26",
    "bets": [
        {
            "type": "prop",
            "event": {
                "sport": "Basketball",
            },
            "bookDescription": "Denver Nuggets @ Los Angeles Lakers - To Score 25+ Points - Anthony Davis",
        },
        {
            "type": "straight",
            "event": {
                "sport": "Tennis",
            },
            "bookDescription": "Grigor Dimitrov vs Jannik Sinner - Winner - Jannik Sinner",
        },
    ],
}


class TestFormatBetslips:

    def test_format_betslip_single(self):
        out = format_betslip(mock_raw_betslip_single)
        assert isinstance(out, HedgeBetslip)
        assert out.book == "Underdog"
        assert out.time_placed == ""
        assert out.time_closed != ""
        assert out.odds == "+200"
        assert out.wager == 10.0
        assert out.result == Result.loss
        assert out.earnings == -10.0
        assert out.selection == "ARI @ PHI - Merrill Kelly Strikeouts O/U - lower 5.0"
        assert out.sport == "Baseball"
        assert out.bet_type == "prop"
        assert out.parlay_details == ""

    def test_format_betslip_parlay(self):
        out = format_betslip(mock_raw_betslip_parlay)
        assert isinstance(out, HedgeBetslip)
        assert out.book == "Fanduel"
        assert out.time_placed != ""
        assert out.time_closed != ""
        assert out.odds == "+1572"
        assert out.wager == 125.0
        assert out.result == Result.loss
        assert out.earnings == -125.0
        assert out.selection == ""
        assert out.sport == ""
        assert out.bet_type == "parlay"
        assert out.parlay_details != ""
        assert len(out.parlay_details) == 2
