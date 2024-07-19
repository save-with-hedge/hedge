"""
Wrapper around MongoDB for
  - Fetching/updating raw bets
  - Fetching/updating formatted bets
  - Fetching/updating user stats
"""

import certifi
import os

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from utils.constants import MONGO_DB, MONGO_STATS_COLLECTION, MONGO_USERS_COLLECTION, MONGO_ADMINS_COLLECTION

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
        self.admins_collection = self.database[MONGO_ADMINS_COLLECTION]

    def ping(self):
        try:
            self.client.admin.command("ping")
            print("Ping successful!")
        except Exception as e:
            print(e)

    def is_admin(self, username, password):
        admin = self.admins_collection.find_one({username: {"password": password}})
        if admin:
            return True
        return False

    @staticmethod
    def insert_document(collection, document):
        collection.insert_one(document)

    def get_user(self, internal_id):
        """
        :return: A dictionary of user info, or None if the user does not exist
        """
        return self.users_collection.find_one({internal_id: {"$exists": True}})

    def create_user(self, internal_id, first, last, phone):
        document = {
            internal_id: {
                "first": first,
                "last": last,
                "phone": phone,
            }
        }
        self.users_collection.insert_one(document)


if __name__ == "__main__":
    # For testing locally only
    repository = MongoRepository()
    repository.ping()

