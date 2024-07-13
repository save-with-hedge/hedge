"""
Usage: 
    python3 get_custom_url.py [user_id (default: ncolosso)] [sportsbook: fanduel/draftkings/underdog (default:fanduel)]
"""
import os
import sys
from dotenv import load_dotenv

from service.sharp_sports_service import SharpSportsService
from utils.constants import INTERNAL_ID_NICO

load_dotenv()


def get_custom_url(internal_id, book_region_id=None):

    # Create service client
    sharp_sports_service = SharpSportsService(internal_id, os.getenv("SHARPSPORTS_PUBLIC_API_KEY"), os.getenv("SHARPSPORTS_PRIVATE_API_KEY"))
    sharp_sports_service.create_extension_auth_token()

    # Create context
    cid = sharp_sports_service.create_context()

    # Create url
    custom_url = f"https://ui.sharpsports.io/link/{cid}"
    if book_region_id:
        custom_url += f"/region/{book_region_id}/login"
    return custom_url


def print_usage():
    print(f"\nUsage:\n\npython3 betsync/get_custom_url.py [user_id (default: ncolosso)] [sportsbook: fanduel/draftkings/underdog (default:fanduel)]\n")


if __name__ == "__main__":

    if (len(sys.argv) > 1 and sys.argv[1].lower() == "help"):
        print_usage()
        exit()

    internal_id = INTERNAL_ID_NICO
    if (len(sys.argv) > 1):
        internal_id = sys.argv[1]

    book = "Fanduel"
    book_region_id = os.getenv("FANDUEL_NY_ID")
    if (len(sys.argv) > 2):
        if sys.argv[2].lower() not in ["fanduel", "draftkings", "underdog"]:
            print_usage()
            exit()
        elif sys.argv[2].lower() == "draftkings":
            book = "Draftkings"
            book_region_id = os.getenv("DRAFTKINGS_NY_ID")
        elif sys.argv[2].lower() == "underdog":
            book = "Underdog"
            book_region_id = os.getenv("UNDERDOG_NY_ID")

    url = get_custom_url(internal_id, book_region_id=book_region_id)
    print(f"\nCustom url for {internal_id}, {book}: {url}")
