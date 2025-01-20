import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def get_database_connection():
    client = MongoClient(os.getenv("MONGO_CLIENT_URL"))["order-service"]

    return client
