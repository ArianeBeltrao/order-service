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

    def create_order(self, orderRequest: OrderRequest) -> str:
        try:
            self.logger.info("Creating order...")

            customer = self.customer.get_customer_by_email(orderRequest.customer_email)

            products_data = []
            for product in orderRequest.products:
                product = self.product.get_product_by_name(product.name)

                products_data.append(product)

            order = Order(customer=customer, products=products_data)

            return self.storage.create_order(order)

        except Exception as e:
            self.logger.error(f"Failed to create order: {e}")
            raise

    def get_orders_by_customer_id(self, customer_id: str) -> Orders:
        try:
            self.logger.info("Getting orders by customer id...")

            return self.storage.get_orders_by_customer_id(customer_id)

        except Exception as e:
            self.logger.error(f"Failed to get orders by customer id: {e}")
            raise
