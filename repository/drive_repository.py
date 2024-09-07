"""
Wrapper around Google Drive client
"""
import os

from dotenv import load_dotenv
from googleapiclient.discovery import build, Resource
from google.oauth2 import service_account
from typing import List, Any

from models.hedge_betslip import HedgeBetslip
from utils.csv_utils import write_csv
from utils.log import get_logger
from utils.path_anchor import BETSLIPS_FORMATTED_FOLDER, PROJECT_ROOT


LOGGER = get_logger("DriveRepository")

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/drive"]
SERVICE_ACCT_FILE = str(PROJECT_ROOT / "service_account.json")
PARENT_FOLDER_ID = os.getenv("GOOGLE_DRIVE_DATA_FOLDER_ID")


class DriveRepository:

    def __init__(self):
        self.out_dir = BETSLIPS_FORMATTED_FOLDER
        self.creds = self.authenticate()

    def authenticate(self) -> Any:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCT_FILE, scopes=SCOPES)
        return creds

    def delete_file(self, service: Resource, filename: str) -> None:
        query = f"name = '{filename}'"
        results = service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
        items = results.get("files", [])
        for item in items:
            service.files().delete(fileId=item["id"]).execute()

    def upload(self, filepath: str) -> None:
        with build("drive", "v3", credentials=self.creds) as service:
            filename = filepath.split("/")[-1]
            file_metadata = {
                "name": filename,
                "parents": [PARENT_FOLDER_ID]
            }
            try:
                self.delete_file(service=service, filename=filename)  # Replace the old file if it exists
                service.files().create(
                    body=file_metadata,
                    media_body=filepath,
                ).execute()
            except Exception as e:
                LOGGER.error(f"Failed to upload betslips file {filename}: {e}")

    def upload_betslips(self, filename: str, betslips: List[HedgeBetslip]) -> None:
        """
        Writes a list of HedgeBetslip to a CSV file and uploads it to Google Drive
        """
        betslip_dicts = [betslip.__dict__ for betslip in betslips]
        fieldnames = list(betslip_dicts[0].keys())
        path = str(BETSLIPS_FORMATTED_FOLDER / filename)
        write_csv(filepath=path, rows=betslip_dicts, fieldnames=fieldnames)
        self.upload(filepath=path)


if __name__ == '__main__':
    """
    For testing purposes only
    """
    drive_repo = DriveRepository()
    drive_repo.upload(filepath=str(BETSLIPS_FORMATTED_FOLDER / "ncolosso.csv"))
