import logging
import os

import httpx

from models.order import Product


class ProductClient:
    def __init__(self, client_http: httpx):
        self.logger = logging.getLogger(__name__)
        self.client_http = client_http

    def get_product_by_name(self, product_name: str) -> Product:
        try:
            self.logger.info(f"Getting product by name={product_name}")
            product_url = f"{os.getenv('PRODUCT_BASE_URL')}{os.getenv('PRODUCT_GET_BY_NAME_PATH')}{product_name}"

            product_response = self.client_http.get(product_url)
            self.logger.debug(f"Get product by name response: {product_response}")

            product_response.raise_for_status()

            return Product(**product_response.json())

        except httpx.RequestError as e:
            self.logger.error(f"Failed to get product by name: {e}")
            raise
