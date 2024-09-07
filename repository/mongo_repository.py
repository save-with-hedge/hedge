"""
Wrapper around MongoDB
"""
import certifi
import json
import requests
import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from utils.constants import (
    MONGO_USERS_COLLECTION,
    MONGO_ADMINS_COLLECTION, MONGO_STATS_COLLECTION,
)
from utils.log import get_logger

LOGGER = get_logger("MongoRepository")

load_dotenv()
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
MONGO_DB = os.getenv("MONGO_DB")
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
        self.stats_collection = self.database[MONGO_STATS_COLLECTION]
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

    def _insert_document(self, collection, document):
        url = self.api_url + "/insertOne"
        payload = json.dumps(
            {
                "dataSource": MONGO_CLUSTER,
                "database": MONGO_DB,
                "collection": collection,
                "document": document,
            }
        )
        LOGGER.info(f"Request: {url}")
        response = requests.request("POST", url, headers=self.api_headers, data=payload)
        LOGGER.info(f"Response: {response.text}")
        if response.status_code not in [200, 201]:
            LOGGER.error(response.text)

    def upsert_document(self, collection, internal_id, document):
        url = self.api_url + "/updateOne"
        payload = json.dumps(
            {
                "dataSource": MONGO_CLUSTER,
                "database": MONGO_DB,
                "collection": collection,
                "filter": {"internal_id": internal_id},
                "update": document,
                "upsert": True,
            }
        )
        LOGGER.info(f"Request: {url}")
        response = requests.request("POST", url, headers=self.api_headers, data=payload)
        LOGGER.info(f"Response: {response.text}")
        if response.status_code not in [200, 201]:
            LOGGER.error(response.text)

    def find_document(self, collection, search_filter):
        url = self.api_url + "/findOne"
        payload = json.dumps(
            {
                "dataSource": MONGO_CLUSTER,
                "database": MONGO_DB,
                "collection": collection,
                "filter": search_filter,
            }
        )
        LOGGER.info(f"Request: {url}")
        response = requests.request("POST", url, headers=self.api_headers, data=payload)
        if response.status_code not in [200, 201]:
            LOGGER.error(f"Response: {response.text}")
        else:
            LOGGER.info(f"Response: {response.text}")
        response_dict = json.loads(response.text)
        return response_dict.get("document")

    def is_admin(self, username, password):
        is_admin = self.find_document(
            MONGO_ADMINS_COLLECTION, {"username": username, "password": password}
        )
        if is_admin:
            LOGGER.info("Mongo: User authenticated as admin")
            return True
        LOGGER.info("Mongo failed to authenticate user as admin")
        return False

    def get_bettor(self, internal_id):
        """
        :return: A dictionary of bettor info, or None if the bettor does not exist
        """
        return self.find_document(MONGO_USERS_COLLECTION, {"internal_id": internal_id})

    def create_bettor(self, internal_id, first, last, phone):
        document = {
            "internal_id": internal_id,
            "first": first,
            "last": last,
            "phone": phone,
        }
        self._insert_document(MONGO_USERS_COLLECTION, document)


if __name__ == "__main__":
    # For testing locally only
    repository = MongoRepository()
    repository.create_bettor("ncolosso", "Nico", "Colosso", 6509963840)
