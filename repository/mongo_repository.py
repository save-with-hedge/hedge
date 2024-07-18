"""
Wrapper around MongoDB for
  - Fetching/updating raw bets
  - Fetching/updating formatted bets
  - Fetching/updating user stats
"""

import certifi
import logging
import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from utils.constants import MONGO_DB, MONGO_STATS_COLLECTION, MONGO_USERS_COLLECTION

load_dotenv()


class MongoRepository:
    uri = (
        f"mongodb+srv://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASSWORD")}@hedgecluster.mhcxijz.mongodb.net"
        f"/?retryWrites=true&w=majority&appName=HedgeCluster"
    )

    def __init__(self):
        self.client = MongoClient(
            self.uri, server_api=ServerApi("1"), tlsCAFile=certifi.where()
        )
        self.database = self.client[MONGO_DB]
        self.bettor_stats_collection = self.database[MONGO_STATS_COLLECTION]
        self.users_collection = self.database[MONGO_USERS_COLLECTION]

    def ping(self):
        try:
            self.client.admin.command("ping")
            print("Ping successful!")
        except Exception as e:
            print(e)

    def get_user(self, internal_id):
        """
        :return: A dictionary of user info, or None if the user does not exist
        """
        key = {"users": internal_id}
        return self.users_collection.find_one(key)

    def create_user(self, internal_id, first, last, phone):
        document = {
            "user": {
                internal_id: {
                    "first": first,
                    "last": last,
                    "phone": phone,
                }
            }
        }
        self.users_collection.insert_one(document)


if __name__ == "__main__":
    repository = MongoRepository()
    repository.ping()
