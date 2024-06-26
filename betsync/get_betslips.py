import json
import os
import sys
from dotenv import load_dotenv

from betsync_client import BetSyncClient
from constants import INTERNAL_ID_NICO

load_dotenv()

def get_betslips(internal_id):

    # Create BetSync client
    betsync_client = BetSyncClient(internal_id, os.getenv("SHARPSPORTS_PUBLIC_API_KEY"), os.getenv("SHARPSPORTS_PRIVATE_API_KEY"))

    # Get bettorAccount id
    bettor_accounts = betsync_client.get_bettor_accounts()
    bettor_account_id = bettor_accounts[0].get("id")

    # Pull betslips
    betslips = betsync_client.get_betslips_by_bettor_account(bettor_account_id)
    return betslips

def print_usage():
    print(f"\nUsage:\n\npython3 betsync/get_betslips.py [user_id (default: ncolosso)]\n")


if __name__ == "__main__":
    
    if (len(sys.argv) > 1 and sys.argv[1].lower() == "help"):
        print_usage()
        exit()

    internal_id = INTERNAL_ID_NICO
    if (len(sys.argv) > 1):
        internal_id = sys.argv[1]

    betslips = get_betslips(internal_id)
    print(betslips)
