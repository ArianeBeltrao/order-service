import logging
import os

import requests

from models.order import Customer
from models.order_request import OrderRequest


class CustomerClient:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_customer_by_email(self, orderRequest: OrderRequest):
        try:
            self.logger.info("Getting customer by email...")

            customer_url = f"{os.getenv('CUSTOMER_BASE_URL')}{os.getenv('CUSTOMER_GET_BY_EMAIL_PATH')}{orderRequest.customer_email}"
            customer_response = requests.get(customer_url)

            self.logger.debug(f"Get customer by email response: {customer_response}")

            if customer_response.status_code == 404:
                raise ValueError(
                    f"Customer not found with email {orderRequest.customer_email}"
                )

            customer = Customer(**customer_response.json())

            return customer

        except requests.RequestException as e:
            self.logger.error(f"Failed to get customer by email: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to get customer by email in general: {e}")
            raise
