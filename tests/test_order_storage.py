from unittest.mock import AsyncMock, MagicMock

import pytest
from pymongo.errors import PyMongoError
from pytest import fixture

from storages.order_storage import OrderStorage


@fixture(name="db_collection")
def fixture_db_collection():
    return MagicMock()


@fixture(name="db_conn")
def fixture_db_conn(db_collection):
    db = MagicMock()
    db.get_collection.return_value = db_collection
    return db


@fixture(name="async_db_conn")
def fixture_async_db_conn(db_collection):
    db = MagicMock()
    db.return_value = db_collection
    return db


@fixture(name="storage")
def fixture_storage(db_conn, async_db_conn):
    return OrderStorage(db_conn, async_db_conn)


@pytest.mark.asyncio
async def test_v2_create_order(storage, order, order_id, db_collection):
    db_collection.insert_one = AsyncMock(return_value=MagicMock(inserted_id=order_id))

    storage.async_collection = AsyncMock()
    storage.async_collection.insert_one = AsyncMock(
        return_value=MagicMock(inserted_id=order_id)
    )

    result = await storage.v2_create_order(order)

    assert result == order_id

    storage.async_collection.insert_one.assert_called_once_with(order.model_dump())


@pytest.mark.asyncio
async def test_v2_create_order_pymongo_error(storage, order, db_collection, order_id):
    db_collection.insert_one = AsyncMock(side_effect=PyMongoError())

    storage.async_collection = db_collection

    with pytest.raises(PyMongoError):
        await storage.v2_create_order(order)


def test_create_order(storage, order, order_id, db_collection):
    db_collection.insert_one.return_value.inserted_id = order_id

    result = storage.create_order(order)

    assert result == order_id

    db_collection.insert_one.assert_called_once_with(order.model_dump())


def test_create_order_pymongo_error(storage, order, db_collection):
    db_collection.insert_one.side_effect = PyMongoError()

    with pytest.raises(PyMongoError):
        storage.create_order(order)


def test_get_orders_by_customer_id(
    db_collection, storage, orders, orders_dict, customer_id
):
    db_collection.find.return_value = orders_dict

    result = storage.get_orders_by_customer_id(customer_id)

    assert result == orders


def test_get_orders_by_customer_id_pymongo_error(db_collection, storage, customer_id):
    db_collection.find.side_effect = PyMongoError()

    with pytest.raises(PyMongoError):
        storage.get_orders_by_customer_id(customer_id)


def test_delete_order_by_id(storage, order_id):
    result = storage.delete_order_by_id(order_id)
    assert result is None


def test_delete_order_by_id_value_error(db_collection, storage, order_id):
    db_collection.delete_one.return_value = MagicMock(deleted_count=0)

    with pytest.raises(ValueError):
        storage.delete_order_by_id(order_id)


def test_delete_order_by_id_pymongo_error(db_collection, storage, order_id):
    db_collection.delete_one.side_effect = PyMongoError()

    with pytest.raises(PyMongoError):
        storage.delete_order_by_id(order_id)
