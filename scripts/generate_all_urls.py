import os

from dotenv import load_dotenv

from scripts.get_custom_url import get_custom_url
from utils.csv_utils import read_csv, write_csv
from utils.path_anchor import CUSTOMER_URLS_FILEPATH

load_dotenv()


def generate_all_urls():
    customer_rows = read_csv(CUSTOMER_URLS_FILEPATH)
    for row in customer_rows:
        if not row["SharpSports Link"] or row["SharpSports Link"] == "":
            continue
        internal_id = row.get("Internal ID")
        fanduel_url = get_custom_url(internal_id, os.getenv("FANDUEL_NY"))
        draftkings_url = ""
        underdog_url = ""
        row["SharpSports Link"] = {
            "fanduel": fanduel_url,
            "draftkings": draftkings_url,
            "underdog": underdog_url,
        }
    fieldnames = list(customer_rows[0].keys())
    # write_csv(CUSTOMER_URLS_FILEPATH, customer_rows, fieldnames)


if __name__ == '__main__':
    generate_all_urls()
