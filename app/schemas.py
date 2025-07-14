from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class OrderCreate(BaseModel):
    customer_name: str = Field(..., example="Jane Doe", min_length=1)
    product_id: int = Field(..., example=42, gt=0)
    quantity: int = Field(..., example=3, gt=0)
    address: str = Field(..., example="123 Main St, Springfield")

class OrderInDB(OrderCreate):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    order: OrderInDB
    class Config:
        schema_extra = {
            "example": {
                "order": {
                    "id": 1,
                    "customer_name": "Jane Doe",
                    "product_id": 42,
                    "quantity": 3,
                    "address": "123 Main St, Springfield",
                    "created_at": "2024-06-15T12:34:56.789Z"
                }
            }
        }

class ErrorResponse(BaseModel):
    detail: str
    class Config:
        schema_extra = {"example": {"detail": "Order ID 123 not found."}}
