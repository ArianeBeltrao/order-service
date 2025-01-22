import os
from unittest.mock import MagicMock

import pytest
import requests
from pytest import fixture

from clients.customer_client import CustomerClient


@fixture(name="customer_requests")
def fixture_customer_requests():
    return MagicMock()


@fixture(name="http_response")
def fixture_http_response():
    return MagicMock()


@fixture(name="customer_client")
def fixture_customer_client(customer_requests):
    return CustomerClient(customer_requests)


@fixture(name="customer_url")
def fixture_customer_url():
    product_url = f"{os.getenv('CUSTOMER_BASE_URL')}{os.getenv('CUSTOMER_GET_BY_EMAIL_PATH')}ana@email.com"
    return product_url


@fixture(name="customer_json")
def fixture_customer_json():
    return {
        "id": "01JH3ZNS5PFG3R1S17N0QX2P18",
        "name": "ana",
        "email": "ana@email.com",
    }


def test_get_customer_by_email(
    customer_requests,
    customer_client,
    customer,
    customer_url,
    customer_json,
    http_response,
):
    http_response.json.return_value = customer_json

    customer_requests.get.return_value = http_response

    result = customer_client.get_customer_by_email("ana@email.com")

    assert result == customer
    customer_requests.get.assert_called_once_with(customer_url)


def test_get_customer_by_email_request_exception(customer_requests, customer_client):
    customer_requests.get.side_effect = requests.RequestException

    with pytest.raises(requests.RequestException):
        customer_client.get_customer_by_email("ana@email.com")

    customer_requests.get.assert_called_once()
