import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from requests.exceptions import HTTPError

from models.order_request import OrderRequest, OrderResponse
from services.order_service import OrderService

router = APIRouter()

logger = logging.getLogger(__name__)


def get_order_service(request: Request):
    return request.state.order_service


ServiceDep = Annotated[OrderService, Depends(get_order_service)]


@router.post(
    "/v1/orders", status_code=status.HTTP_201_CREATED, response_model=OrderResponse
)
def create_order(order: OrderRequest, service: ServiceDep):
    try:
        logger.info("Started CreateOrder")
        order_id = service.create_order(order)

        logger.info(f"CreateOrder route order_id: {order_id}")

        return OrderResponse(id=order_id)

    except HTTPError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=str(e),
        ) from e
