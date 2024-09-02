"""
Fetch a user's raw betslips from Sharp Sports and write the results to json
Usage:
    python3 fetch_betslips.py [user_id (default: ncolosso)]
"""

from service.sharp_sports_service import SharpSportsService
from utils.json_utils import read_json, write_json
from utils.log import get_logger
from utils.path_anchor import BETSLIPS_RAW_FOLDER

LOGGER = get_logger(__name__)


def fetch_betslips(internal_id: str, refresh: bool = True):
    """
    Fetch betslips from Sharp Sports and write raw betslips to json.
    :return: Raw betslips in Sharp Sports format
    """
    # Create BetSync client
    betsync_client = SharpSportsService()

    # Refresh bettor accounts
    if refresh:
        betsync_client.refresh_bettor(internal_id)

    # Pull betslips and write to file
    betslips = betsync_client.get_betslips_by_bettor(internal_id)
    if betslips is None or len(betslips) == 0:
        return []

    filepath = BETSLIPS_RAW_FOLDER + "/" + internal_id + ".json"
    write_json(filepath, betslips)
    return betslips


def fetch_local_betslips(internal_id):
    """
    Fetch betslips from local out/ folder and return
    """
    LOGGER.info(f"fetch_betslips: Fetching local betslips for {internal_id}")
    filepath = BETSLIPS_RAW_FOLDER + "/" + internal_id + ".json"
    betslips = read_json(filepath)
    return betslips
