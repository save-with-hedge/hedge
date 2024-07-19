import json
import requests
import os

from dotenv import load_dotenv


load_dotenv()


class SharpSportsService:

    def __init__(self):
        self.public_api_key = os.getenv("SHARPSPORTS_PUBLIC_API_KEY")
        self.private_api_key = os.getenv("SHARPSPORTS_PRIVATE_API_KEY")
        self.extension_auth_token = ""
        self.base_url = "https://api.sharpsports.io/v1"

    @staticmethod
    def get_headers(api_key, additional_headers=None):
        headers = {"accept": "application/json", "Authorization": f"Token {api_key}"}
        if additional_headers:
            for key, value in additional_headers.items():
                headers[key] = value
        return headers

    def get_book_regions(self):
        url = self.base_url + "/bookRegions?status=active"
        headers = self.get_headers(self.public_api_key)
        print(headers)
        params = {"status": "active"}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"{response.status_code} - {response.text}")
            return
        return json.loads(response.text)

    def get_book_region_detail(self, book_id):
        url = self.base_url + "/bookRegions" + book_id
        headers = self.get_headers(self.public_api_key)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"{response.status_code} - {response.text}")
            return
        return json.loads(response.text)

    def create_extension_auth_token(self, internal_id, platform="extension"):
        """
        For SDK Required books, we must include this token with the create_context request
        """
        url = self.base_url + "/" + platform + "/auth"
        payload = {"internalId": internal_id}
        headers = self.get_headers(
            self.private_api_key, {"content-type": "application/json"}
        )
        print(f"Request: {url}")
        response = requests.post(url, json=payload, headers=headers)
        print(f"Response: {response.text}")
        if response.status_code != 200:
            print(f"{response.status_code} - {response.text}")
            raise
        return json.loads(response.text).get("token")

    def create_context(self, internal_id, auth_token=None):
        url = self.base_url + "/context"
        payload = {
            "uiMode": "system",
            "internalId": internal_id,
        }
        if auth_token:
            payload["extensionAuthToken"] = auth_token
        headers = self.get_headers(
            self.public_api_key, {"content-type": "application/json"}
        )
        print(f"Request: {url}")
        response = requests.post(url, json=payload, headers=headers)
        print(f"Response: {response.text}")
        if response.status_code != 200 and response.status_code != 201:
            print(f"{response.status_code} - {response.text}")
            return
        return json.loads(response.text).get("cid")

    def get_bettors(self):
        url = self.base_url + "/bettors"
        headers = self.get_headers(self.private_api_key)
        response = requests.get(url, headers=headers)
        if response.status_code != 200 and response.status_code != 201:
            print(f"{response.status_code} - {response.text}")
            return
        return json.loads(response.text)

    def get_bettor_accounts(self, internal_id):
        url = self.base_url + "/bettors/" + internal_id + "/bettorAccounts"
        headers = self.get_headers(self.private_api_key)
        response = requests.get(url, headers=headers)
        if response.status_code != 200 and response.status_code != 201:
            print(f"{response.status_code} - {response.text}")
            return
        return json.loads(response.text)

    def refresh_bettor(self, internal_id):
        url = self.base_url + "/bettors/" + internal_id + "/refresh"
        headers = self.get_headers(self.public_api_key)
        response = requests.post(url, headers=headers)
        if response.status_code != 200 and response.status_code != 201:
            print(f"{response.status_code} - {response.text}")
            return

    def get_betslips_by_bettor(
        self, internal_id, status="completed", start_date=None, end_date=None
    ):
        url = self.base_url + "/bettors/" + internal_id + "/betSlips"
        url += f"?status={status}"
        if start_date:
            url += f"&timePlacedStart={start_date}"
        if end_date and start_date:
            url += f"&timePlacedEnd={end_date}"
        elif end_date and start_date is None:
            url += f"&timePlacedEnd={end_date}"
        headers = self.get_headers(self.private_api_key)
        response = requests.get(url, headers=headers)
        if response.status_code != 200 and response.status_code != 201:
            print(f"{response.status_code} - {response.text}")
            return
        return json.loads(response.text)


if __name__ == "__main__":
    # For testing only
    service = SharpSportsService()
    print(service.get_book_regions())
