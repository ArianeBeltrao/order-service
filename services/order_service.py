import logging
import os

from requests import RequestException
import requests
from dotenv import load_dotenv
from models.order import Customer, Order, Product
from models.order_request import OrderRequest
from storages.order_storage import OrderStorage

class OrderService:
    def __init__(self, storage: OrderStorage):
        self.logger = logging.getLogger(__name__)
        self.storage = storage
        load_dotenv()
        
    def create_order(self, orderRequest: OrderRequest):
        try:
            self.logger.info("Creating order...")
            
            customer_url = (
                f"{os.getenv("CUSTOMER_BASE_URL")}{os.getenv("CUSTOMER_GET_BY_EMAIL_PATH")}{orderRequest.customer_email}"
            )
            customer_response = requests.get(customer_url).json()
            self.logger.debug(f"Customer response: {customer_response}")
            
            customer = Customer(**customer_response)
            
            products_data = []
            for product in orderRequest.products:
                product_url = (f"{os.getenv("PRODUCT_BASE_URL")}{os.getenv("PRODUCT_GET_BY_NAME_PATH")}{product.name}")
    
                product_response = requests.get(product_url).json()
                product = Product(**product_response)
                
                products_data.append(product)
                self.logger.debug(f"Product data: {products_data}")
            
            order = Order(customer=customer, products=products_data)
  
            return self.storage.create_order(order)
            
        except RequestException as e:
            self.logger.error(f"Failed to create order and get customer email and products: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to crete order: {e}")
            raise