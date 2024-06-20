import os
import requests
from dotenv import load_dotenv

load_dotenv()
PUBLIC_API_KEY = os.getenv("SHARPSPORTS_PUBLIC_API_KEY")
PRIVATE_API_KEY = os.getenv("SHARPSPORTS_PRIVATE_API_KEY")
INTERNAL_ID = "ncolosso"
FANDUEL_NY_BOOK_ID = "BRGN_ab5628fa79344c39bce8fec0f17fbdcc"


class BetSyncClient:

    def __init__(self, public_api_key, private_api_key):
        self.public_api_key = public_api_key
        self.private_api_key = private_api_key
        self.base_url = "https://api.sharpsports.io/v1"

    @staticmethod
    def get_headers(api_key, additional_headers=None):
        headers = {
            "accept": "application/json",
            "Authorization": f"Token {api_key}"
        }
        if additional_headers:
            for key, value in additional_headers.items():
                headers[key] = value
        return headers

    def create_extension_auth_tokens(self):
        url = self.base_url + "/extension/auth"
        payload = {"internalId": INTERNAL_ID}
        headers = self.get_headers(self.private_api_key, {"content-type": "application/json"})
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"{response.status_code} - {response.text}")
            raise
        return response.text

    def get_book_regions(self):
        url = self.base_url + "/bookRegions"
        headers = self.get_headers(self.public_api_key)
        params = {"status": "active"}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"{response.status_code} - {response.text}")
            return
        return response.text

    def get_book_region_detail(self, book_id):
        url = self.base_url + "/bookRegions" + book_id
        headers = self.get_headers(self.public_api_key)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"{response.status_code} - {response.text}")
            return
        return response.text

    def create_context(self):
        url = self.base_url + "/context"
        payload = {
            "uiMode": "system",
            "internalId": INTERNAL_ID
        }
        headers = self.get_headers(PUBLIC_API_KEY, {"content-type": "application/json"})
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"{response.status_code} - {response.text}")
            return
        return response.text

    def get_bettors(self):
        url = self.base_url + "/bettors"
        headers = self.get_headers(self.private_api_key)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"{response.status_code} - {response.text}")
            return
        return response.text


if __name__ == "__main__":
    client = BetSyncClient(PUBLIC_API_KEY, PRIVATE_API_KEY)
    resp = client.get_book_regions()
    print(resp)
