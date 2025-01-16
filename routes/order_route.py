import logging
from fastapi import APIRouter, Depends, Request, status
from typing import Annotated
from models.order import Order
from models.order_request import OrderRequest
from services.order_service import OrderService

router = APIRouter()

logger = logging.getLogger(__name__)

def get_order_service(request: Request):
    return request.state.order_service

ServiceDep = Annotated[OrderService, Depends(get_order_service)]

@router.post("/v1/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderRequest, service:ServiceDep):
    logger.info(f"Started CreateOrder")
    service.create_order(order)
    return