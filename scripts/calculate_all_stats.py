import datetime

from scripts.calculate_stats import calculate_stats
from service.sharp_sports_service import SharpSportsService
from utils.csv_utils import write_csv
from utils.path_anchor import STATS_FOLDER
from utils.betslip_utils import get_ytd_timedelta


def calculate_all_stats(delta=None):
    # Get internal ids
    internal_ids = get_internal_ids()

    # Calculate stats for each internal_id
    all_stats = []
    for internal_id in internal_ids:
        user_stats = calculate_stats(internal_id, True, delta)
        if len(user_stats) == 0:
            continue
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
    sharp_sports_service = SharpSportsService()
    all_bettors = sharp_sports_service.get_bettors()
    return [bettor.get("internalId") for bettor in all_bettors]


if __name__ == "__main__":
    # delta = datetime.timedelta(days=7)
    delta = get_ytd_timedelta()
    calculate_all_stats(delta)  # YTD
