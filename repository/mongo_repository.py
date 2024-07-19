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
        except Exception as e:
            print(e)

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
        response = requests.request("POST", url, headers=self.api_headers, data=payload)
        admin = json.loads(response.text).get("document")
        # admin = self.admins_collection.find_one({username: {"password": password}})
        if admin:
            return True
        return False

    def insert_document(self, collection, document):
        url = self.api_url + "/insertOne"
        payload = json.dumps({
            "dataSource": MONGO_CLUSTER,
            "database": MONGO_DB,
            "collection": collection,
            "document": document
        })
        response = requests.request("POST", url, headers=self.api_headers, data=payload)
        # collection.insert_one(document)

    def get_user(self, internal_id):
        """
        :return: A dictionary of user info, or None if the user does not exist
        """
        url = self.api_url + "/findOne"
        payload = json.dumps({
            "dataSource": MONGO_CLUSTER,
            "database": MONGO_DB,
            "collection": MONGO_USERS_COLLECTION,
            "filter": {internal_id: {"$exists": True}}
        })
        response = requests.request("POST", url, headers=self.api_headers, data=payload)
        response_dict = json.loads(response.text)
        return response_dict.get("document")
        # return self.users_collection.find_one({internal_id: {"$exists": True}})

    def create_user(self, internal_id, first, last, phone):
        document = {
            internal_id: {
                "first": first,
                "last": last,
                "phone": phone,
            }
        }
        self.insert_document(MONGO_USERS_COLLECTION, document)
        # self.users_collection.insert_one(document)


if __name__ == "__main__":
    # For testing locally only
    repository = MongoRepository()
    resp = repository.get_user("fake-user")
    print(resp)
