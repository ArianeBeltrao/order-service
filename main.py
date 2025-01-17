import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from routes.order_route import router
from services.order_service import OrderService
from storages.order_storage import OrderStorage

logger = logging.getLogger(__name__)
logging.getLogger("pymongo").setLevel(logging.WARNING)


@asynccontextmanager
async def lifespan(app: FastAPI):
    order_storage = OrderStorage()
    order_service = OrderService(order_storage)

    yield {"order_service": order_service}
    logger.info("Shutdown application")


app = FastAPI(lifespan=lifespan, title="Order Service")
app.include_router(router)
