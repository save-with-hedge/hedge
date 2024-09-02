from utils.betslip_utils import *
from utils.log import get_logger

LOGGER = get_logger("CalculateStats")


def calculate_stats(betslips: list[HedgeBetslip]):
    """
    For the given user and timedelta, calculate average unit size and ROI by bet type and write the results to
    json and csv
    """
    if len(betslips) == 0:
        return []

    # Group by bet type
    betslips_grouped = group_betslips_by_bet_type(betslips)

    # Calculate stats
    stats, stats_list = get_stats_for_bets_grouped(betslips, betslips_grouped)

    return stats_list


def get_stats_for_bets_grouped(
    all_betslips: list[HedgeBetslip], betslips_grouped: dict[str, list[HedgeBetslip]]
):
    """
    Calculate stats by bet type and return dictionary and list representations
    :return: a dict (only used for appending to bet history) and list representation of stats by bet type
    """
    stats = {}
    stats_list = [
        {
            "betType": "total",
            "avgUnit": calculate_avg_unit_size(all_betslips),
            "roi": calculate_roi(all_betslips),
            "total_bets": len(all_betslips),
        }
    ]
    for bet_type in betslips_grouped:
        stats[bet_type] = {
            "avgUnit": calculate_avg_unit_size(betslips_grouped.get(bet_type)),
            "roi": calculate_roi(betslips_grouped.get(bet_type)),
        }
        stats_list.append(
            {
                "betType": bet_type,
                "avgUnit": stats.get(bet_type).get("avgUnit"),
                "roi": stats.get(bet_type).get("roi"),
                "total_bets": len(betslips_grouped.get(bet_type)),
            }
        )
    return stats, stats_list
