import os
from unittest.mock import MagicMock

import pytest
import requests
from pytest import fixture

from clients.product_client import ProductClient


@fixture(name="product_requests")
def fixture_product_requests():
    return MagicMock()


@fixture(name="http_response")
def fixture_http_response():
    return MagicMock()


@fixture(name="product_client")
def fixture_product_client(product_requests):
    return ProductClient(product_requests)


@fixture(name="product_url")
def fixture_product_url():
    product_url = (
        f"{os.getenv('PRODUCT_BASE_URL')}{os.getenv('PRODUCT_GET_BY_NAME_PATH')}puzzle"
    )
    return product_url


@fixture(name="product_json")
def fixture_product_json():
    return {
        "id": "01JH3ZNS5PFG3R1S17N0QX2P18",
        "name": "puzzle",
        "description": "500 piece puzzle",
        "price": 10,
        "quantity": 2,
    }


def test_get_product_by_name(
    product_requests, product_client, product, product_url, product_json, http_response
):
    http_response.json.return_value = product_json

    product_requests.get.return_value = http_response

    result = product_client.get_product_by_name("puzzle")

    assert result == product
    product_requests.get.assert_called_once_with(product_url)


def test_get_product_by_name_request_exception(product_requests, product_client):
    product_requests.get.side_effect = requests.RequestException

    with pytest.raises(requests.RequestException):
        product_client.get_product_by_name("puzzle")

    product_requests.get.assert_called_once()
