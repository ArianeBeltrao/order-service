import logging

from pymongo import MongoClient, database
from pymongo.errors import PyMongoError

from models.order import Order, Orders


class OrderStorage:
    def __init__(self, db_connection: MongoClient, async_db_connection):
        self.logger = logging.getLogger(__name__)
        self.db_connection: MongoClient = db_connection
        self.collection: database.Database = self.db_connection.get_collection("order")
        self.async_db_conn = async_db_connection
        self.async_collection = self.async_db_conn["order"]

    async def v2_create_order(self, order: Order) -> str:
        self.logger.info("V2 Inserting order in DB")
        try:
            result = await self.async_collection.insert_one(order.model_dump())

            return str(result.inserted_id)

        except PyMongoError as e:
            self.logger.error(f"Failed to create order in DB. PyMongoError: {e}")
            raise

    def create_order(self, order: Order) -> str:
        self.logger.info("Inserting order in DB")
        try:
            result = self.collection.insert_one(order.model_dump())

            return str(result.inserted_id)

        except PyMongoError as e:
            self.logger.error(f"Failed to create order in DB. PyMongoError: {e}")
            raise

    def get_orders_by_customer_id(self, customer_id: str) -> Orders:
        self.logger.info("Finding orders in DB")
        try:
            result = self.collection.find({"customer.id": customer_id})

            orders = [Order(**order) for order in result]

            return Orders(orders=orders)

        except PyMongoError as e:
            self.logger.error(
                f"Failed to find orders in DB by customer id. PyMongoError: {e}"
            )
            raise

    def delete_order_by_id(self, order_id: str) -> None:
        self.logger.info("Deleting order in DB")
        try:
            result = self.collection.delete_one({"id": order_id})

            if result.deleted_count == 0:
                raise ValueError((f"Order not found with id {order_id}"))

        except PyMongoError as e:
            self.logger.error(
                f"Failed to delete order in DB by order id. PyMongoError: {e}"
            )
            raise
