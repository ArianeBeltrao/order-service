from datetime import datetime
from typing import List

import ulid
from pydantic import BaseModel, EmailStr, Field


class Customer(BaseModel):
    id: str = Field(
        default_factory=lambda: str(ulid.new()), description="Customer ulid"
    )
    name: str = Field(description="Customer name")
    email: EmailStr = Field(description="Customer email")


class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(ulid.new()), description="Product ulid")
    name: str = Field(description="Product name")
    description: str = Field(description="Product description")
    price: float = Field(gt=0, description="The price must be greater than zero")
    quantity: int = Field(description="Product quantity")


class Order(BaseModel):
    id: str = Field(default_factory=lambda: str(ulid.new()), description="Product ulid")
    customer: Customer
    products: List[Product]
    created_at: datetime = Field(
        default_factory=datetime.now, description="Create product timestamp"
    )
    updated_at: datetime | None = Field(
        default=None, description="Update product timestamp"
    )


class Orders(BaseModel):
    orders: List[Order]
