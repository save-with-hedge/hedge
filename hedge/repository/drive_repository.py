"""
Wrapper around Google Drive client
"""
from googleapiclient.discovery import build
from typing import List

from hedge.models.hedge_betslip import HedgeBetslip
from hedge.utils.csv_utils import write_csv
from hedge.utils.path_anchor import BETSLIPS_FORMATTED_FOLDER


class DriveRepository:

    def __init__(self):
        self.out_dir = BETSLIPS_FORMATTED_FOLDER

    def ping(self):
        with build('drive', 'v3') as service:
            pass

    def upload_betslips(self, filename: str, betslips: List[HedgeBetslip]) -> None:
        """
        Writes a list of HedgeBetslip to a CSV file and uploads it to Google Drive
        """
        betslip_dicts = [betslip.__dict__ for betslip in betslips]
        fieldnames = list(betslip_dicts[0].keys())
        path = str(BETSLIPS_FORMATTED_FOLDER / filename)
        write_csv(filepath=path, rows=betslip_dicts, fieldnames=fieldnames)


if __name__ == '__main__':
    drive_repo = DriveRepository()
    drive_repo.ping()
