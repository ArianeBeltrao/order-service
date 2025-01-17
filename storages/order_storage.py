import logging

from pymongo import MongoClient

from models.order import Order


class OrderStorage:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = MongoClient("mongodb://order:order@localhost:27017/admin")
        self.db_connection = self.client["order-service"]

        self.collection = self.db_connection.get_collection("order")

    def create_order(self, order: Order):
        result = self.collection.insert_one(order.model_dump())
        self.logger.info(f"Inserting order in DB with the order request: {result}")

        return result.inserted_id
