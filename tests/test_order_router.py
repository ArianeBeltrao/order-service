from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from pytest import fixture

from main import app
from routes.order_router import get_order_service


@fixture(name="service")
def fixture_service():
    """
    Creates a mock service object to simulate the product service layer.

    Returns:
        MagicMock: A mock service object.
    """
    return MagicMock()


@fixture(name="client")
def fixture_client(service):
    app.dependency_overrides[get_order_service] = lambda: service
    client = TestClient(app)
    return client


def test_router_create_order(
    service, client, order_request, order_id, order_request_json, order_response_json
):
    service.create_order.return_value = order_id
    response = client.post("/v1/orders", json=order_request_json)

    assert response.status_code == 201
    assert response.json() == order_response_json

    service.create_order.assert_called_once_with(order_request)


def test_router_create_order_value_error(
    service, client, order_request, order_request_json
):
    service.create_order.side_effect = ValueError()
    response = client.post("/v1/orders", json=order_request_json)

    assert response.status_code == 404
    service.create_order.assert_called_once_with(order_request)
