from scripts.calculate_stats import calculate_stats
from utils.csv_utils import write_csv
from utils.path_anchor import STATS_FOLDER


def calculate_all_stats():
    # Get internal ids
    internal_ids = get_internal_ids()

    # Calculate stats for each internal_id
    all_stats = []
    for internal_id in internal_ids:
        user_stats = calculate_stats(internal_id, True)
        for bet_type_stats in user_stats:
            all_stats_row = {
                "internalId": internal_id,
                "betType": bet_type_stats.get("betType"),
                "avgUnit": bet_type_stats.get("avgUnit"),
                "roi": bet_type_stats.get("roi"),
            }
            all_stats.append(all_stats_row)

    # Write to csv
    filepath = STATS_FOLDER + "/all_stats"
    fieldnames = list(all_stats[0].keys())
    write_csv(f"{filepath}.csv", all_stats, fieldnames)
    print(f"Wrote {len(all_stats)} rows to {filepath}")


def get_internal_ids():
    return ["ncolosso", "ryan_murphy", "henry_armistead"]


if __name__ == '__main__':
    calculate_all_stats()
