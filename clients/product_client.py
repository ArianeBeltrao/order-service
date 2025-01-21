import logging
import os

import requests

from models.order import Product


class ProductClient:
    def __init__(self, requests):
        self.logger = logging.getLogger(__name__)
        self.requests = requests

    def get_product_by_name(self, product_name: str):
        try:
            self.logger.info(f"Getting product by name={product_name}")

            product_url = f"{os.getenv('PRODUCT_BASE_URL')}{os.getenv('PRODUCT_GET_BY_NAME_PATH')}{product_name}"

            product_response = self.requests.get(product_url)

            self.logger.debug(f"Get product by name response: {product_response}")

            if product_response.status_code == 404:
                raise ValueError(f"Product not found with name={product_name}")

            product = Product(**product_response.json())

            return product

        except requests.RequestException as e:
            self.logger.error(f"Failed to get product by name: {e}")
            raise
