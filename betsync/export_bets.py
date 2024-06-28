"""
Fetch a user's bet history from Sharp Sports and export the formatted bets to a csv file.
Csv files are written to the hedge/out/ folder and named bet_history_[user_id].csv

Usage:
    python3 export_bets.py [user_id (default: ncolosso)]
"""
import csv
import os
import sys
from dotenv import load_dotenv

from betsync_client import BetSyncClient
from constants import INTERNAL_ID_NICO, OUTPUT_FOLDER, BET_HISTORY_FILE_PREFIX

load_dotenv()

def get_betslips(internal_id):

    # Create BetSync client
    betsync_client = BetSyncClient(internal_id, os.getenv("SHARPSPORTS_PUBLIC_API_KEY"), os.getenv("SHARPSPORTS_PRIVATE_API_KEY"))

    # Get bettorAccount id
    bettor_accounts = betsync_client.get_bettor_accounts()
    bettor_account_id = bettor_accounts[0].get("id")

    # Pull betslips
    betslips = betsync_client.get_betslips_by_bettor_account(bettor_account_id)
    return betslips

def process_betslips(betslips):
    processed_bets = []
    for betslip in betslips:
        processed_bet = {
            "time": betslip.get("timePlaced"),
            "selection": "",
            "sport": "",
            "betSlipType": betslip.get("type"),
            "betType": "",
            "odds": betslip.get("oddsAmerican"),
            "stake": betslip.get("atRisk"),
            "result": betslip.get("outcome"),
            "return": betslip.get("netProfit"),
        }
        if processed_bet.get("betSlipType") == "single":
            bet = betslip.get("bets")[0]
            event = bet.get("event")
            processed_bet["selection"] = bet.get("bookDescription")
            processed_bet["betType"] = bet.get("type")
            processed_bet["sport"] = event.get("sport")
        elif processed_bet.get("betSlipType") == "parlay":
            processed_bet["selection"] = "parlay"
            processed_bet["betType"] = "parlay"
            processed_bet["sport"] = "parlay"
        if processed_bet.get("betType") is None:
            processed_bet["betType"] = "*"
        processed_bets.append(processed_bet)
    return processed_bets

def export_bets(bets, filename):
    # Write bets to csv
    fieldnames = ["time", "selection", "sport", "betSlipType", "betType", "odds", "stake", "result", "return"]
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for bet in bets:
            writer.writerow(bet)

def print_usage():
    print(f"\nUsage:\n\npython3 betsync/export_bets.py [user_id (default: ncolosso)]\n")


if __name__ == "__main__":
    
    if (len(sys.argv) > 1 and sys.argv[1].lower() == "help"):
        print_usage()
        exit()

    internal_id = INTERNAL_ID_NICO
    if (len(sys.argv) > 1):
        internal_id = sys.argv[1]

    output_filename = OUTPUT_FOLDER + "/" + BET_HISTORY_FILE_PREFIX + "_" + internal_id + ".csv"

    betslips = get_betslips(internal_id)
    processed_bets = process_betslips(betslips)
    export_bets(processed_bets, output_filename)
    print(f"Wrote {len(processed_bets)} rows to file {output_filename}")
