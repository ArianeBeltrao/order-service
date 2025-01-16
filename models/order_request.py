from pydantic import BaseModel, EmailStr, Field
from typing import List

class ProductRequest(BaseModel):
    name: str = Field(description="Product name")
    quantity: int = Field(description="Product quantity")
    
class OrderRequest(BaseModel):
    customer_email: EmailStr = Field(description="Customer email")
    products: List[ProductRequest]