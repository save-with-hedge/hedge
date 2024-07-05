from datetime import datetime

from utils.constants import BETSLIP_RESULTS_DATE_FORMAT, SHARP_API_REQUEST_DATE_FORMAT


def get_past_date_formatted(delta):
    """
    Get formatted datetime string with timedelta applied
    """
    past_date = datetime.today() - delta
    return past_date.strftime(SHARP_API_REQUEST_DATE_FORMAT)


def filter_betslips_by_timestamp(betslips, delta):
    """
    Note: this algo is not optimized for performance, but should be fine for the time being
    """
    start_date = datetime.today() - delta
    filtered_betslips = []
    for betslip in betslips:
        date = datetime.strptime(betslip.get("time"), BETSLIP_RESULTS_DATE_FORMAT)
        if date >= start_date:
            filtered_betslips.append(betslip)
    return filtered_betslips


def group_betslips_by_bet_type(betslips):
    """
    Return a dictionary where each key is a betType and each value is the list of betSlips for that betType
    """
    pass


def group_betslips_by_betslip_type(betslips):
    """
    Return a dictionary where each key is a betSlipType and each value is the list of betSlips for that betSlipType
    """
    pass


def calculate_avg_unit_size(betslips):
    wager_sum = 0
    for betslip in betslips:
        wager_sum += float(betslip.get("wager"))
    return wager_sum / len(betslips)


def calculate_roi(betslips):
    """
    ROI = net return as a % of total wager
    """
    wager_sum = 0
    net_return = 0
    for betslip in betslips:
        wager_sum += float(betslip.get("wager"))
        net_return += float(betslip.get("return"))
    return wager_sum / net_return


def get_decimal_from_odds(odds):
    if odds > 0:
        return float(1 + (odds / 100))
    elif odds < 0:
        return float(1 + (100 / abs(odds)))
    return 0.0
