"""
Usage:
    python3 fetch_betslips.py [user_id (default: ncolosso)]
"""
import os
import sys
from dotenv import load_dotenv

from service.sharp_sports_service import SharpSportsService
from utils.constants import INTERNAL_ID_NICO
from utils.json_utils import write_json
from utils.path_anchor import BETSLIPS_RAW_FOLDER, BETSLIPS_FORMATTED_FOLDER

load_dotenv()


def fetch_betslips(internal_id):
    """
    Fetch betslips from Sharp Sports and write raw betslips to json.
    """
    # Create BetSync client
    betsync_client = SharpSportsService(internal_id, os.getenv("SHARPSPORTS_PUBLIC_API_KEY"),
                                        os.getenv("SHARPSPORTS_PRIVATE_API_KEY"))

    # Refresh bettor accounts
    betsync_client.refresh_bettor()

    # Pull betslips and write to file
    betslips = betsync_client.get_betslips_by_bettor()
    filepath = BETSLIPS_RAW_FOLDER + "/" + internal_id + ".json"
    write_json(filepath, betslips)
    print(f"Wrote {len(betslips)} rows to file {filepath}")

    return betslips


def format_bets(raw_betslips, internal_id):
    """
    Format the raw betslips from Sharp Sports and write to json.
    """
    formatted_bets = []
    for betslip in raw_betslips:
        formatted_bet = {
            "book": betslip.get("book").get("name"),
            "time": betslip.get("timePlaced"),
            "selection": "",
            "sport": "",
            "betType": "",
            "propDetails": "",
            "odds": betslip.get("oddsAmerican"),
            "wager": float(betslip.get("atRisk")) / 100,
            "result": betslip.get("outcome"),
            "return": float(betslip.get("netProfit")) / 100,
        }
        if betslip.get("type") == "single":
            bet = betslip.get("bets")[0]
            formatted_bet["selection"] = bet.get("bookDescription")
            if bet.get("event"):
                formatted_bet["sport"] = bet.get("event").get("sport")
            if not bet.get("type"):
                formatted_bet["betType"] = "other"
            if bet.get("type") == "straight":
                formatted_bet["betType"] = bet.get("proposition")
            elif bet.get("type") == "prop":
                formatted_bet["betType"] = "other"
                formatted_bet["propDetails"] = bet.get("propDetails")
        elif betslip.get("type") == "parlay":
            formatted_bet["selection"] = "parlay"
            formatted_bet["sport"] = "parlay"
            formatted_bet["betType"] = "parlay"
        formatted_bets.append(formatted_bet)

    json_filepath = BETSLIPS_FORMATTED_FOLDER + "/" + internal_id + ".json"
    write_json(json_filepath, formatted_bets)
    print(f"Wrote {len(formatted_bets)} rows to file {json_filepath}")

    return formatted_bets


def print_usage():
    print(f"\nUsage:\n\npython3 betsync/fetch_betslips.py [user_id (default: ncolosso)]\n")


if __name__ == "__main__":

    if (len(sys.argv) > 1 and sys.argv[1].lower() == "help"):
        print_usage()
        exit()

    internal_id = INTERNAL_ID_NICO
    if (len(sys.argv) > 1):
        internal_id = sys.argv[1]

    raw_betslips = fetch_betslips(internal_id)
    # raw_betslips = read_json(BETSLIPS_RAW_FOLDER + "/" + internal_id + ".json")
    formatted_bets = format_bets(raw_betslips, internal_id)
