"""
Calculate a user's performance for a given window, using the bet history located at hedge/bet_history_[user_id].csv.
Current performance metrics:
    Win %
    ROI
    Net Return
Performance metrics are written to the hedge/out/ folder and named past_performance_[user_id].csv

Usage:
    python3 calculate_performance.py [user_id (default: ncolosso)]
"""
import csv
import json
import sys

from constants import INTERNAL_ID_NICO, OUTPUT_FOLDER, BET_HISTORY_FILE_PREFIX, PERFORMANCE_FILE_PREFIX

def calculate_performance(internal_id):
    # TODO filter by time window
    # Read bet performance into Dict
    bet_history_filename = OUTPUT_FOLDER + "/" + BET_HISTORY_FILE_PREFIX + "_" + internal_id + ".csv"
    bet_history = read_csv(bet_history_filename)

    # Loop through bets and get metrics for all permutations of sport|betSlipType|betType
    bet_performance_dict = {}
    for bet in bet_history:
        key = "|".join([bet.get("sport"), bet.get("betSlipType"), bet.get("betType")])
        if key not in bet_performance_dict:
            bet_performance_dict[key] = {"win_count": 0, "loss_count": 0, "push_count": 0, "net_return": 0.0}
        update_metrics(bet_performance_dict[key], bet)
    print(json.dumps(bet_performance_dict, indent=2))

    # Output metrics

def read_csv(filepath):
    rows = []
    with open(filepath, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rows.append(row)
    return rows

def update_metrics(bet_metrics, bet):
    result = bet.get("result").lower()
    net_return = float(bet.get("return")) / 100
    if result == "win":
        bet_metrics["win_count"] += 1
    elif result == "loss":
        bet_metrics["loss_count"] += 1
    elif result == "push":
        bet_metrics["push_count"] += 1
    bet_metrics["net_return"] += net_return

def export_metrics():
    # Write metrics to csv
    print("")

def print_usage():
    print(f"\nUsage:\n\npython3 betsync/calculate_performance.py [user_id (default: ncolosso)]\n")


if __name__ == "__main__":

    if (len(sys.argv) > 1 and sys.argv[1].lower() == "help"):
        print_usage()
        exit()

    internal_id = INTERNAL_ID_NICO
    if (len(sys.argv) > 1):
        internal_id = sys.argv[1]

    output_filename = OUTPUT_FOLDER + "/" + PERFORMANCE_FILE_PREFIX + "_" + internal_id + ".csv"
    
    calculate_performance(internal_id)
