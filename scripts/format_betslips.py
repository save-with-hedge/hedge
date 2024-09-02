from datetime import datetime
from typing import List

from models.hedge_betslip import HedgeBetslip, Result
from scripts.fetch_betslips import fetch_betslips, fetch_local_betslips
from utils.log import get_logger

LOGGER = get_logger("FormatBetSlips")


def format_betslips(internal_id, fetch=True, refresh=False) -> List[HedgeBetslip]:
    raw_betslips = (
        fetch_betslips(internal_id, refresh)
        if fetch
        else fetch_local_betslips(internal_id)
    )
    formatted_betslips = []
    for betslip in raw_betslips:
        try:
            formatted_betslips.append(format_betslip(betslip))
        except Exception as e:
            LOGGER.error(
                f"format_betslips: Error formatting {internal_id} betslip {betslip.get('id')}: {e}"
            )
    return formatted_betslips


def format_betslips(raw_betslips) -> List[HedgeBetslip]:
    """
    Format a user's raw json betslips into Hedge format
    :return: A list of HedgeBetslip objects
    """
    formatted_betslips = []
    for betslip in raw_betslips:
        try:
            formatted_betslips.append(format_betslip(betslip))
        except Exception as e:
            LOGGER.error(
                f"format_betslips: Error formatting betslip {betslip.get('id')}: {e}"
            )
    return formatted_betslips


def format_betslip(raw_betslip):
    """
    :param raw_betslip: a raw, Sharp Sports betslip
    :return: a HedgeBetslip object
    """
    betslip_type = _get_attr(raw_betslip, "type", None)
    if betslip_type is None:
        raise Exception("Betslip has no type attribute")
    if betslip_type == "single":
        return get_single_type_hedge_object(raw_betslip)
    elif betslip_type == "parlay":
        return get_parlay_type_hedge_object(raw_betslip)
    else:
        raise Exception(
            f"Betslip type {betslip_type} not supported (only single and parlay allowed)"
        )


def get_single_type_hedge_object(raw_betslip):
    hedge_object = get_base_hedge_object(raw_betslip)
    single_bet = _get_attr(raw_betslip, "bets", None)
    if single_bet is None:
        raise Exception("Betslip has no bets attribute")
    single_bet = single_bet[0]
    selection = _get_attr(single_bet, "bookDescription", "")
    bet_type = _get_attr(single_bet, "type", "other")
    sport = _get_attr(_get_attr(single_bet, "event", {}), "sport", "")
    hedge_object.selection = selection
    hedge_object.bet_type = bet_type
    hedge_object.sport = sport
    return hedge_object


def get_parlay_type_hedge_object(raw_betslip):
    hedge_object = get_base_hedge_object(raw_betslip)
    hedge_object.bet_type = "parlay"
    bets_list = _get_attr(raw_betslip, "bets", None)
    if bets_list:
        hedge_object.parlay_details = format_parlay_details(bets_list)
    return hedge_object


def format_parlay_details(bets_list):
    """
    :param bets_list: raw bets list from betslip.get("bets")
    :return: a list of bet objects containing bet description
    """
    parlay_details = []
    for bet in bets_list:
        if bet.get("bookDescription"):
            parlay_details.append(bet.get("bookDescription"))
    return parlay_details


def get_base_hedge_object(raw_betslip):
    book_name = _get_attr(_get_attr(raw_betslip, "book", ""), "name", "")
    time_placed = _get_attr(raw_betslip, "timePlaced", "")
    time_closed = _get_attr(raw_betslip, "timeClosed", "")
    if time_closed == "":
        date_closed_raw = _get_attr(raw_betslip, "dateClosed", "")
        if date_closed_raw != "":
            date_closed_datetime = datetime.strptime(date_closed_raw, "%Y-%m-%d")
            time_closed = date_closed_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    odds = _get_attr(raw_betslip, "oddsAmerican", "")
    odds = _format_odds_str(odds)
    at_risk = _get_attr(raw_betslip, "atRisk", None)
    wager = 0.0
    if at_risk:
        wager = float(at_risk) / 100
    net_profit = _get_attr(raw_betslip, "netProfit", None)
    earnings = 0.0
    if net_profit:
        earnings = float(net_profit) / 100
    result = format_result(_get_attr(raw_betslip, "outcome", None))
    return HedgeBetslip(
        book=book_name,
        time_placed=time_placed,
        time_closed=time_closed,
        odds=odds,
        wager=wager,
        result=result,
        earnings=earnings,
        selection="",
        sport="",
        bet_type="",
        parlay_details="",
    )


def format_result(raw_outcome):
    if raw_outcome is None:
        raise Exception("Betslip has no outcome field")
    elif raw_outcome == "win":
        return Result.win
    elif raw_outcome == "loss":
        return Result.loss
    elif raw_outcome == "push":
        return Result.push
    else:
        raise Exception(
            f"Betslip outcome {raw_outcome} not supported (only win, loss, push allowed)"
        )


def _get_attr(dict_obj, attr, default=None):
    if dict_obj.get(attr) is None:
        return default
    else:
        return dict_obj.get(attr)


def _format_odds_str(odds):
    if odds == "":
        return ""
    elif odds >= 0:
        return f"+{odds}"
    elif odds < 0:
        return f"{odds}"
