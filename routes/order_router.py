import logging
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status

from models.order import Orders
from models.order_request import OrderRequest, OrderResponse
from services.order_service import OrderService

router = APIRouter()

logger = logging.getLogger(__name__)


def get_order_service(request: Request):
    return request.state.order_service


ServiceDep = Annotated[OrderService, Depends(get_order_service)]


@router.post(
    "/v2/orders", status_code=status.HTTP_201_CREATED, response_model=OrderResponse
)
async def v2_create_order(order: OrderRequest, service: ServiceDep):
    try:
        logger.info("V2 Started CreateOrder")
        order_id = await service.v2_create_order(order)

        logger.info(f"V2 CreateOrder request finished with response: {order_id}")
        return OrderResponse(id=order_id)

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=str(e),
        ) from e


@router.post(
    "/v1/orders", status_code=status.HTTP_201_CREATED, response_model=OrderResponse
)
def create_order(order: OrderRequest, service: ServiceDep):
    try:
        logger.info("Started CreateOrder")
        order_id = service.create_order(order)

        logger.info(f"CreateOrder request finished with response: {order_id}")
        return OrderResponse(id=order_id)

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=str(e),
        ) from e


@router.get("/v1/orders/customer/{customer_id}", response_model=Orders)
def get_orders_by_customer_id(customer_id: str, service: ServiceDep):
    logger.info(f"Started GetOrders with customer id={customer_id}")
    orders_data = service.get_orders_by_customer_id(customer_id)

    logger.info(f"GetOrders request finished with response={orders_data}")
    return orders_data


@router.delete("/v1/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order_by_id(order_id: str, service: ServiceDep):
    try:
        logger.info(f"Started DeleteOrder with order id={order_id}")
        service.delete_order_by_id(order_id)

        logger.info(f"DeleteOrder request finished for order id={order_id}")
        return
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order not found with id {order_id}",
        ) from e
