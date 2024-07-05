import json
import requests


class BetSyncClient:

    def __init__(self, internal_id, public_api_key, private_api_key):
        self.internal_id = internal_id
        self.public_api_key = public_api_key
        self.private_api_key = private_api_key
        self.extension_auth_token = ""
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

    def create_extension_auth_token(self, platform="extension"):
        url = self.base_url + "/" + platform + "/auth"
        payload = {"internalId": self.internal_id}
        headers = self.get_headers(self.private_api_key, {"content-type": "application/json"})
        print(f"Request: {url}")
        response = requests.post(url, json=payload, headers=headers)
        print(f"Response: {response.text}")
        if response.status_code != 200:
            print(f"{response.status_code} - {response.text}")
            raise
        self.extension_auth_token = json.loads(response.text).get("token")

    def get_book_regions(self):
        url = self.base_url + "/bookRegions?status=active"
        headers = self.get_headers(self.public_api_key)
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

    def create_context(self):
        url = self.base_url + "/context"

        auth_token = self.extension_auth_token
        payload = {
            "uiMode": "system",
            "internalId": self.internal_id,
            "extensionAuthToken": auth_token,
        }
        headers = self.get_headers(self.public_api_key, {"content-type": "application/json"})
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
    
    def get_bettor_accounts(self):
        url = self.base_url + "/bettors/" + self.internal_id + "/bettorAccounts"
        headers = self.get_headers(self.private_api_key)
        response = requests.get(url, headers=headers)
        if response.status_code != 200 and response.status_code != 201:
            print(f"{response.status_code} - {response.text}")
            return
        return json.loads(response.text)

    def get_betslips_by_bettor_account(self, bettor_account_id, start_date=None, end_date=None):
        url = self.base_url + "/bettorAccounts/" + bettor_account_id + "/betSlips"
        if start_date:
            url += f"?timePlacedStart={start_date}"
        if end_date and start_date:
            url += f"&timePlacedEnd={end_date}"
        elif end_date and start_date is None:
            url += f"?timePlacedEnd={end_date}"
        headers = self.get_headers(self.private_api_key)
        response = requests.get(url, headers=headers)
        if response.status_code != 200 and response.status_code != 201:
            print(f"{response.status_code} - {response.text}")
            return
        return json.loads(response.text)
