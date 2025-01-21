from unittest.mock import MagicMock

import pytest
from pytest import fixture

from services.order_service import OrderService


@fixture(name="storage")
def fixture_storage():
    return MagicMock()


@fixture(name="customer_client")
def fixture_customer_client():
    return MagicMock()


@fixture(name="product_client")
def fixture_product_client():
    return MagicMock()


@fixture(name="service")
def fixture_service(storage, customer_client, product_client):
    return OrderService(storage, customer_client, product_client)


def test_create_order_successfully(
    service,
    storage,
    order_id,
    customer_client,
    product_client,
    order_request,
    customer,
    product,
):
    customer_client.get_customer_by_email.return_value = customer
    product_client.get_product_by_name.return_value = product
    storage.create_order.return_value = order_id

    result = service.create_order(order_request)

    assert result == order_id

    customer_client.get_customer_by_email.assert_called_once_with("ana@email.com")
    product_client.get_product_by_name.assert_called_once_with("puzzle")

    storage.create_order.assert_called_once()


def test_create_order_handles_exception(
    service, storage, order_request, customer_client, customer, product_client, product
):
    storage.create_order.side_effect = Exception()
    customer_client.get_customer_by_email.return_value = customer
    product_client.get_product_by_name.return_value = product

    with pytest.raises(Exception):
        service.create_order(order_request)

    storage.create_order.assert_called_once()
