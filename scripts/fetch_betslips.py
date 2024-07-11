"""
Usage:
    python3 fetch_betslips.py [user_id (default: ncolosso)]
"""
import os
import sys
from dotenv import load_dotenv

from betsync_service import BetSyncClient
from utils.constants import INTERNAL_ID_NICO
from utils.csv_utils import write_csv
from utils.json_utils import write_json, read_json
from utils.path_anchor import BETSLIPS_RAW_FOLDER, BETSLIPS_FORMATTED_FOLDER

load_dotenv()


def fetch_betslips(internal_id):
    """
    Fetch betslips from Sharp Sports and write raw betslips to json.
    """
    # Create BetSync client
    betsync_client = BetSyncClient(internal_id, os.getenv("SHARPSPORTS_PUBLIC_API_KEY"),
                                   os.getenv("SHARPSPORTS_PRIVATE_API_KEY"))

    # Get bettorAccount id
    bettor_accounts = betsync_client.get_bettor_accounts()
    bettor_account_id = bettor_accounts[0].get("id")

    # Pull betslips and write to file
    betslips = betsync_client.get_betslips_by_bettor_account(bettor_account_id)
    filepath = BETSLIPS_RAW_FOLDER + "/" + internal_id + ".json"
    write_json(filepath, betslips)
    print(f"Wrote {len(betslips)} rows to file {filepath}")

    return betslips


def format_bets(raw_betslips):
    """
    Format the raw betslips from Sharp Sports and write to json.
    """
    formatted_bets = []
    for betslip in raw_betslips:
        bet = {
            "time": betslip.get("timePlaced"),
            "selection": "",
            "sport": "",
            "betSlipType": betslip.get("type"),
            "betType": "",
            "odds": betslip.get("oddsAmerican"),
            "wager": float(betslip.get("atRisk")) / 100,
            "result": betslip.get("outcome"),
            "return": float(betslip.get("netProfit")) / 100,
        }
        if bet.get("betSlipType") == "single":
            bet_raw = betslip.get("bets")[0]
            bet["selection"] = bet_raw.get("bookDescription")
            if bet_raw.get("type") == "straight" and bet_raw.get("proposition"):
                bet["betType"] = bet_raw.get("proposition")
            else:
                bet["betType"] = bet_raw.get("type")
            event = bet_raw.get("event")
            if event:
                bet["sport"] = event.get("sport")
        elif bet.get("betSlipType") == "parlay":
            bet["selection"] = "parlay"
            bet["betType"] = "parlay"
            bet["sport"] = "parlay"
        formatted_bets.append(bet)

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

    # raw_betslips = fetch_betslips(internal_id)
    raw_betslips = read_json(BETSLIPS_RAW_FOLDER + "/" + internal_id + ".json")
    formatted_bets = format_bets(raw_betslips)
