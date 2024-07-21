"""
Wrapper around MongoDB for
  - Fetching/updating raw bets
  - Fetching/updating formatted bets
  - Fetching/updating user stats
"""

import certifi
import json
import requests
import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from utils.constants import MONGO_DB, MONGO_STATS_COLLECTION, MONGO_USERS_COLLECTION, MONGO_ADMINS_COLLECTION
from utils.log import get_logger

LOGGER = get_logger()

load_dotenv()
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_API_KEY = os.getenv("MONGO_API_KEY")


class MongoRepository:
    uri = (
        f"mongodb+srv://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASSWORD")}@hedgecluster.mhcxijz.mongodb.net"
        f"/?retryWrites=true&w=majority&appName=HedgeCluster"
    )
    api_url = "https://us-east-1.aws.data.mongodb-api.com/app/data-ciszpbd/endpoint/data/v1/action"
    api_headers = headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": os.getenv("MONGO_API_KEY"),
    }

    def __init__(self):
        self.client = MongoClient(
            self.uri, server_api=ServerApi("1"), tlsCAFile=certifi.where()
        )
        self.database = self.client[MONGO_DB]
        self.bettor_stats_collection = self.database[MONGO_STATS_COLLECTION]
        self.users_collection = self.database[MONGO_USERS_COLLECTION]
        self.admins_collection = self.database[MONGO_ADMINS_COLLECTION]

    def ping(self):
        try:
            self.client.admin.command("ping")
            print("Ping successful!")
            return "Ping successful!"
        except Exception as e:
            print(e)
            return str(e)

    def is_admin(self, username, password):
        url = self.api_url + "/findOne"
        payload = json.dumps({
            "dataSource": MONGO_CLUSTER,
            "database": MONGO_DB,
            "collection": MONGO_ADMINS_COLLECTION,
            "filter": {
                username: {"password": password}
            }
        })
        LOGGER.info(f"Mongo request: {url}")
        response = requests.request("POST", url, headers=self.api_headers, data=payload)
        LOGGER.info(f"Mongo response: {response.text}")
        admin = json.loads(response.text).get("document")
        if admin:
            LOGGER.info("Mongo: User authenticated as admin")
            return True
        LOGGER.info("Mongo failed to authenticate user as admin")
        return False

    def insert_document(self, collection, document):
        LOGGER.info(f"Inserting mongo document to {collection}")
        url = self.api_url + "/insertOne"
        payload = json.dumps({
            "dataSource": MONGO_CLUSTER,
            "database": MONGO_DB,
            "collection": collection,
            "document": document
        })
        LOGGER.info(f"Mongo request: {url}")
        response = requests.request("POST", url, headers=self.api_headers, data=payload)
        LOGGER.info(f"Mongo response: {response.text}")
        if response.status_code not in [200, 201]:
            LOGGER.error(response.text)

    def get_user(self, internal_id):
        """
        :return: A dictionary of user info, or None if the user does not exist
        """
        LOGGER.info(f"Fetching mongo user {internal_id}")
        url = self.api_url + "/findOne"
        payload = json.dumps({
            "dataSource": MONGO_CLUSTER,
            "database": MONGO_DB,
            "collection": MONGO_USERS_COLLECTION,
            "filter": {internal_id: {"$exists": True}}
        })
        LOGGER.info(f"Mongo request: {url}")
        response = requests.request("POST", url, headers=self.api_headers, data=payload)
        LOGGER.info(f"Mongo response: {response.text}")
        if response.status_code not in [200, 201]:
            LOGGER.error(response.text)
        LOGGER.info(f"Mongo response {response.text}")
        response_dict = json.loads(response.text)
        return response_dict.get("document")

    def create_user(self, internal_id, first, last, phone):
        document = {
            internal_id: {
                "first": first,
                "last": last,
                "phone": phone,
            }
        }
        self.insert_document(MONGO_USERS_COLLECTION, document)


if __name__ == "__main__":
    # For testing locally only
    repository = MongoRepository()
    resp = repository.get_user("fake-user")
    print(resp)
