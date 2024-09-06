"""
Wrapper around Google Drive client
"""
from googleapiclient.discovery import build
from google.oauth2 import service_account
from typing import List, Any

from hedge.models.hedge_betslip import HedgeBetslip
from hedge.utils.csv_utils import write_csv
from hedge.utils.path_anchor import BETSLIPS_FORMATTED_FOLDER, PROJECT_ROOT

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCT_FILE = str(PROJECT_ROOT / "service_account.json")
FILE_PATH = str(BETSLIPS_FORMATTED_FOLDER / "andrew_schleeter.csv")
PARENT_FOLDER_ID = "1wNlPwpZi5TdDJqls9N-7IYH-GEyttyz0"  # TODO make this an env variable


class DriveRepository:

    def __init__(self):
        self.out_dir = BETSLIPS_FORMATTED_FOLDER
        self.creds = self.authenticate()

    def authenticate(self) -> Any:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCT_FILE, scopes=SCOPES)
        return creds

    def ping(self):
        with build("drive", "v3", credentials=self.creds) as service:
            file_metadata = {
                "name": "andrew_schleeter.csv",
                "parents": [PARENT_FOLDER_ID]
            }
            service.files().create(
                body=file_metadata,
                media_body=FILE_PATH,
            ).execute()

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
