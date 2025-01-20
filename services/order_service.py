import logging

from dotenv import load_dotenv
from requests import RequestException

from clients.customer_client import CustomerClient
from clients.product_client import ProductClient
from models.order import Order
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
        load_dotenv()

    def create_order(self, orderRequest: OrderRequest):
        try:
            self.logger.info("Creating order...")

            customer = self.customer.get_customer_by_email(orderRequest)

            products_data = []
            for product in orderRequest.products:
                product = self.product.get_product_by_name(product.name)

                products_data.append(product)

            order = Order(customer=customer, products=products_data)

            return self.storage.create_order(order)

        except RequestException as e:
            self.logger.error(
                f"Failed to create order and get customer email and products: {e}"
            )
            raise
        except Exception as e:
            self.logger.error(f"Failed to create order: {e}")
            raise
