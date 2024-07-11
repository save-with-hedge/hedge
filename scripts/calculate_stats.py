"""
Usage:
    python3 calculate_stats.py [user_id (default: ncolosso)]
"""
import sys

from utils.constants import INTERNAL_ID_NICO
from utils.betslip_utils import *
from utils.csv_utils import write_csv
from utils.json_utils import read_json, write_json
from utils.path_anchor import BETSLIPS_FORMATTED_FOLDER, STATS_FOLDER


def calculate_stats(user_id, timedelta=None):
    """
    For the given user and timedelta, calculate average unit size and ROI by bet type and write the results to
    json and csv
    """
    # Get bets for user_id
    bets_filepath = BETSLIPS_FORMATTED_FOLDER + "/" + user_id + ".json"
    bets = read_json(bets_filepath)

    # Filter by timedelta
    if timedelta:
        bets = filter_betslips_by_timestamp(bets, timedelta)

    # Group by bet type
    bets_grouped = group_betslips_by_bet_type(bets)

    # Calculate stats
    stats = {}
    for bet_type in bets_grouped:
        stats[bet_type] = {
            "avgUnit": calculate_avg_unit_size(bets_grouped.get(bet_type)),
            "roi": calculate_roi(bets_grouped.get(bet_type)),
        }

    # Append unit size to bets list
    for bet in bets:
        bet_type = bet.get("betType")
        bet["avgUnit"] = stats.get(bet_type).get("avgUnit")
        bet["roi"] = stats.get(bet_type).get("roi")

    # Write to json and csv
    stats_json = STATS_FOLDER + "/" + user_id + ".json"
    write_json(stats_json, stats)
    print(f"Wrote stats to {stats_json}")

    csv_filepath = BETSLIPS_FORMATTED_FOLDER + "/" + internal_id + ".csv"
    fieldnames = list(bets[0].keys())
    write_csv(csv_filepath, bets, fieldnames)
    print(f"Wrote betslips t0 {csv_filepath}")


def print_usage():
    print(f"\nUsage:\n\npython3 betsync/calculate_stats.py [user_id (default: ncolosso)]\n")


if __name__ == "__main__":

    if (len(sys.argv) > 1 and sys.argv[1].lower() == "help"):
        print_usage()
        exit()

    internal_id = INTERNAL_ID_NICO
    if (len(sys.argv) > 1):
        internal_id = sys.argv[1]

    calculate_stats(internal_id)
