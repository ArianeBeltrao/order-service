import logging
import os

import requests

from models.order import Customer


class CustomerClient:
    def __init__(self, requests):
        self.logger = logging.getLogger(__name__)
        self.requests = requests

    def get_customer_by_email(self, customer_email: str):
        try:
            self.logger.info(f"Getting customer by email={customer_email}")
            customer_url = f"{os.getenv('CUSTOMER_BASE_URL')}{os.getenv('CUSTOMER_GET_BY_EMAIL_PATH')}{customer_email}"

            customer_response = self.requests.get(customer_url)
            self.logger.debug(f"Get customer by email response: {customer_response}")

            customer_response.raise_for_status()

            return Customer(**customer_response.json())

        except requests.RequestException as e:
            self.logger.error(f"Failed to get customer by email: {e}")
            raise
