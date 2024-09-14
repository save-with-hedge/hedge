"""
Fetch a user's raw betslips from Sharp Sports and write the results to json
Usage:
    python3 fetch_betslips.py [user_id (default: ncolosso)]
"""

from app.service.sharp_sports_service import SharpSportsService
from app.utils.json_utils import read_json
from app.utils.log import get_logger
from app.utils.path_anchor import BETSLIPS_RAW_FOLDER

LOGGER = get_logger(__name__)


def fetch_betslips(internal_id: str, refresh: bool = True):
    """
    Fetch betslips from Sharp Sports
    :return: Raw betslips in Sharp Sports format
    """
    # Create BetSync client
    betsync_client = SharpSportsService()

    # Refresh bettor accounts
    if refresh:
        betsync_client.refresh_bettor(internal_id)

    betslips = betsync_client.get_betslips_by_bettor(internal_id)
    if betslips is None or len(betslips) == 0:
        return []
    return betslips


def fetch_local_betslips(internal_id):
    """
    Fetch betslips from local out/ folder and return
    """
    LOGGER.info(f"fetch_betslips: Fetching local betslips for {internal_id}")
    filepath = BETSLIPS_RAW_FOLDER + "/" + internal_id + ".json"
    betslips = read_json(filepath)
    return betslips
