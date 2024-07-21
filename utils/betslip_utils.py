from datetime import datetime

from utils.constants import BETSLIP_RESULTS_DATE_FORMAT, SHARP_API_REQUEST_DATE_FORMAT


def get_past_date_formatted(delta):
    """
    :param delta: timedelta
    """
    past_date = datetime.today() - delta
    return past_date.strftime(SHARP_API_REQUEST_DATE_FORMAT)


def filter_betslips_by_timestamp(betslips, delta):
    """
    This algo is not optimized for performance, but should be fine for the time being
    :param betslips: dictionary of betslips
    :param delta: timedelta
    :return: list of betslips
    """
    start_date = datetime.today() - delta
    filtered_betslips = []
    for betslip in betslips:
        if not betslip.get("timeClosed"):  # TODO clean this up
            continue
        date = datetime.strptime(betslip.get("timeClosed"), BETSLIP_RESULTS_DATE_FORMAT)
        if date >= start_date:
            filtered_betslips.append(betslip)
    return filtered_betslips


def group_betslips_by_bet_type(betslips):
    """
    Return a dictionary where each key is a betType and each value is the list of betSlips for that betType
    :param betslips: dictionary of betslips
    """
    grouped_betslips = {}
    for betslip in betslips:
        bet_type = betslip.get("betType")
        if bet_type not in grouped_betslips:
            grouped_betslips[bet_type] = []
        grouped_betslips[bet_type].append(betslip)
    return grouped_betslips


def calculate_avg_unit_size(betslips):
    """
    :param betslips: dictionary of betslips
    """
    wager_sum = 0
    for betslip in betslips:
        wager_sum += float(betslip.get("wager"))
    return round(wager_sum / len(betslips), 2)


def calculate_roi(betslips):
    """
    ROI = net return as a % of total wager
    :param betslips: dictionary of betslips
    """
    wager_sum = 0
    net_return = 0
    for betslip in betslips:
        wager_sum += float(betslip.get("wager"))
        net_return += float(betslip.get("return"))
    return round((100 * net_return / wager_sum), 2)


def get_decimal_from_odds(odds):
    decimal = 0.0
    if odds > 0:
        decimal = float(1 + (odds / 100))
    elif odds < 0:
        decimal = float(1 + (100 / abs(odds)))
    return round(decimal, 2)


def get_ytd_timedelta():
    current_date = datetime.now()
    jan_1 = datetime(current_date.year, 1, 1)
    delta = current_date - jan_1
    return delta
