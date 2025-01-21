import logging
from contextlib import asynccontextmanager

import requests
from fastapi import FastAPI

from clients.customer_client import CustomerClient
from clients.product_client import ProductClient
from configs.db_conn import get_database_connection
from routes.order_router import router
from services.order_service import OrderService
from storages.order_storage import OrderStorage

logger = logging.getLogger(__name__)
logging.getLogger("pymongo").setLevel(logging.WARNING)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = get_database_connection()
    order_storage = OrderStorage(db_connection)

    customer_client = CustomerClient(requests)
    product_client = ProductClient(requests)

    order_service = OrderService(order_storage, customer_client, product_client)

    yield {"order_service": order_service}
    logger.info("Shutdown application")


app = FastAPI(lifespan=lifespan, title="Order Service")
app.include_router(router)
