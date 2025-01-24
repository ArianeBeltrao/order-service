import os

import motor.motor_asyncio
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()


def get_database_connection() -> MongoClient:
    client = MongoClient(os.getenv("MONGO_CLIENT_URL"))["order-service"]

    return client


def get_async_db_connection() -> motor.motor_asyncio.AsyncIOMotorDatabase:
    client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_CLIENT_URL"))[
        "order-service"
    ]

    return client
