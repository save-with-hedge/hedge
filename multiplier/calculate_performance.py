"""
Calculate a user's performance for a given window, using the bet history located at hedge/bet_history_[user_id].csv.
Current performance metrics:
    Win %
    ROI
Performance metrics are written to the hedge/out/ folder and named past_performance_[user_id].csv

Usage:
    python3 calculate_performance.py [user_id (default: ncolosso)]
"""
import sys

from constants import INTERNAL_ID_NICO, OUTPUT_FOLDER, PERFORMANCE_FILE_PREFIX

def calculate_performance(internal_id):
    # TODO filter by time window
    # Read bet performance into Dict

    # Loop through bets and get metrics for all permutations of sport|betSlipType|betType

    # Output metrics
    print("")

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
