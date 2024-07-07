"""
Fetch a user's bet history from Sharp Sports and export the formatted bets to a csv file.
Csv files are written to the hedge/out/ folder and named bet_history_[user_id].csv

Usage:
    python3 fetch_betslips.py [user_id (default: ncolosso)]
"""
import csv
import os
import sys
from dotenv import load_dotenv

from betsync_client import BetSyncClient
from utils.constants import INTERNAL_ID_NICO, BET_HISTORY_FILE_PREFIX
from utils.csv_utils import write_csv
from utils.json_utils import write_json
from utils.path_anchor import OUTPUT_FOLDER, BETSLIPS_RAW_FOLDER, BETSLIPS_FORMATTED_FOLDER

load_dotenv()


def fetch_betslips(internal_id):
    # Create BetSync client
    betsync_client = BetSyncClient(internal_id, os.getenv("SHARPSPORTS_PUBLIC_API_KEY"),
                                   os.getenv("SHARPSPORTS_PRIVATE_API_KEY"))

    # Get bettorAccount id
    bettor_accounts = betsync_client.get_bettor_accounts()
    bettor_account_id = bettor_accounts[0].get("id")

    # Pull betslips and write to csv
    betslips = betsync_client.get_betslips_by_bettor_account(bettor_account_id)


    return betslips


def format_betslips(betslips):
    processed_bets = []
    for betslip in betslips:
        processed_bet = {
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
        if processed_bet.get("betSlipType") == "single":
            bet = betslip.get("bets")[0]
            processed_bet["selection"] = bet.get("bookDescription")
            processed_bet["betType"] = bet.get("type")
            event = bet.get("event")
            if event:
                processed_bet["sport"] = event.get("sport")
        elif processed_bet.get("betSlipType") == "parlay":
            processed_bet["selection"] = "parlay"
            processed_bet["betType"] = "parlay"
            processed_bet["sport"] = "parlay"
        if processed_bet.get("betType") is None:
            processed_bet["betType"] = "*"
        processed_bets.append(processed_bet)
    return processed_bets


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
    raw_output_file = BETSLIPS_RAW_FOLDER + "/" + internal_id + ".json"
    write_json(raw_output_file, raw_betslips)
    print(f"Wrote {len(raw_betslips)} rows to file {raw_output_file}")

    formatted_bets = format_betslips(raw_betslips)
    formatted_output_file = BETSLIPS_FORMATTED_FOLDER + "/" + internal_id + ".json"
    # fieldnames = list(formatted_bets[0].keys())
    write_json(formatted_output_file, formatted_bets)
    print(f"Wrote {len(formatted_bets)} rows to file {formatted_output_file}")
