"""
Usage: 
    python3 get_custom_url.py [user_id (default: ncolosso)]
"""

import os
import sys
from dotenv import load_dotenv

from service.sharp_sports_service import SharpSportsService
from utils.constants import INTERNAL_ID_NICO

load_dotenv()
FANDUEL_ID = os.getenv("FANDUEL_NY_ID")
DRAFTKINGS_ID = os.getenv("DRAFTKINGS_NY_ID")
UNDERDOG_ID = os.getenv("UNDERDOG_NY_ID")
BETMGM_ID = os.getenv("BETMGM_NY_ID")


def get_custom_url(internal_id):

    # Create service client
    sharp_sports_service = SharpSportsService()
    sharp_sports_service.create_extension_auth_token()

    # Create context
    cid = sharp_sports_service.create_context()

    # Create urls
    urls = {
        "Fanduel": f"https://ui.sharpsports.io/link/{cid}/region/{FANDUEL_ID}/login",
        "Draftkings": f"https://ui.sharpsports.io/link/{cid}/region/{DRAFTKINGS_ID}/login",
        "BetMGM": f"https://ui.sharpsports.io/link/{cid}/region/{BETMGM_ID}/login",
        "Underdog": f"https://ui.sharpsports.io/link/{cid}/region/{UNDERDOG_ID}/login",
    }
    return cid, urls


def print_usage():
    print(
        f"\nUsage:\n\npython3 betsync/get_custom_url.py [user_id (default: ncolosso)]\n"
    )


if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1].lower() == "help":
        print_usage()
        exit()

    internal_id = INTERNAL_ID_NICO
    if len(sys.argv) > 1:
        internal_id = sys.argv[1]

    cid, urls = get_custom_url(internal_id)
    print(f"\nCid: {cid}")
    for key in urls:
        print(f"{key}: {urls.get(key)}")
