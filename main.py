import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.order_route import router
from services.order_service import OrderService
from storages.order_storage import OrderStorage

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_connection = None
    order_storage = OrderStorage(db_connection)
    order_service = OrderService(order_storage)
    
    yield {"order_service": order_service}
    logger.info("Shutdown application")
    
app = FastAPI(
    lifespan=lifespan,
    title="Order Service"
)
app.include_router(router)