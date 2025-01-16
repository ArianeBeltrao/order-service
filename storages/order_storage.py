import logging

from models.order import Order



class OrderStorage:
    def __init__(self, db_connection):
        self.logger = logging.getLogger(__name__)
        self.db = db_connection
        
    def create_order(self, order:Order):
        self.logger.info(f"Inserting order in DB with the order request: {order}")