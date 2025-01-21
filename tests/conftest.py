from datetime import datetime

from pytest import fixture

from models.order import Customer, Order, Product
from models.order_request import OrderRequest


@fixture(name="customer")
def fixture_customer():
    return Customer(id="01JH3ZNS5PFG3R1S17N0QX2P18", name="ana", email="ana@email.com")


@fixture(name="product")
def fixture_product():
    return Product(
        id="01JH3ZNS5PFG3R1S17N0QX2P18",
        name="puzzle",
        description="500 piece puzzle",
        price=10,
        quantity=2,
    )


@fixture(name="order_id")
def fixture_order_id():
    return "678e64681e88dc843b618c67"


@fixture(name="order_response_json")
def fixture_order_response_json(order_id):
    return {"id": order_id}


@fixture(name="order_request_json")
def fixture_order_request_json():
    return {
        "customer_email": "ana@email.com",
        "products": [{"name": "puzzle", "quantity": 2}],
    }


@fixture(name="order_request")
def fixture_order_request():
    return OrderRequest(
        customer_email="ana@email.com",
        products=[
            {
                "name": "puzzle",
                "quantity": 2,
            },
        ],
    )


@fixture(name="order")
def fixture_order(order_id, customer, product):
    return Order(
        id=order_id,
        customer=customer,
        products=[product],
        created_at=datetime(2024, 12, 23, 15, 57, 25, 496623),
        updated_at=None,
    )
