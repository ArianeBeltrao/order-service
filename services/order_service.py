import asyncio
import logging

from clients.customer_client import CustomerClient
from clients.product_client import ProductClient
from models.order import Order, Orders
from models.order_request import OrderRequest
from storages.order_storage import OrderStorage


class OrderService:
    def __init__(
        self, storage: OrderStorage, customer: CustomerClient, product: ProductClient
    ):
        self.logger = logging.getLogger(__name__)
        self.storage = storage
        self.customer = customer
        self.product = product

    async def v2_create_order(self, orderRequest: OrderRequest) -> str:
        try:
            self.logger.info("V2 Creating order...")

            customer_task = self.customer.v2_get_customer_by_email(
                orderRequest.customer_email
            )

            product_tasks = [
                self.product.v2_get_product_by_name(product.name)
                for product in orderRequest.products
            ]

            customer, products = await asyncio.gather(
                customer_task, asyncio.gather(*product_tasks)
            )

            order = Order(customer=customer, products=products)

            return await self.storage.v2_create_order(order)

        except Exception as e:
            self.logger.error(f"Failed to create order: {e}")
            raise

    def create_order(self, orderRequest: OrderRequest) -> str:
        try:
            self.logger.info("Creating order...")

            customer = self.customer.get_customer_by_email(orderRequest.customer_email)

            products = []
            for product in orderRequest.products:
                product = self.product.get_product_by_name(product.name)

                products.append(product)

            order = Order(customer=customer, products=products)

            return self.storage.create_order(order)

        except Exception as e:
            self.logger.error(f"Failed to create order: {e}")
            raise

    def get_orders_by_customer_id(self, customer_id: str) -> Orders:
        self.logger.info("Getting orders by customer id...")

        return self.storage.get_orders_by_customer_id(customer_id)

    def delete_order_by_id(self, order_id: str) -> None:
        self.logger.info("Deleting order by id...")
        self.storage.delete_order_by_id(order_id)
