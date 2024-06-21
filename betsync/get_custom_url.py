import os
from dotenv import load_dotenv

from betsync.betsync_client import BetSyncClient

load_dotenv()
INTERNAL_ID = "ncolosso"
BOOK_REGION_ID = os.getenv("FANDUEL_NY_ID")


def get_custom_ur(book_region_id):

    # Create betsync client
    betsync_client = BetSyncClient(INTERNAL_ID, book_region_id, os.getenv("SHARPSPORTS_PUBLIC_API_KEY"),
                                   os.getenv("SHARPSPORTS_PRIVATE_API_KEY"))
    betsync_client.create_extension_auth_token()

    # Create context
    cid = betsync_client.create_context()

    # Create url
    custom_url = f"https://ui.sharpsports.io/link/{cid}/region/{book_region_id}/login"
    return custom_url


if __name__ == "__main__":
    url = get_custom_ur(BOOK_REGION_ID)
    print(f"\nCustom url for {INTERNAL_ID}: {url}")
