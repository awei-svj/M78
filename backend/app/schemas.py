from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class UserCreate(BaseModel):
    id: Optional[str]
    phone: str
    email: Optional[str] = None

class AddressCreate(BaseModel):
    user_id: str
    name: str
    phone: str
    full_address: str
    is_default: Optional[bool] = False

class SubscribeReq(BaseModel):
    user_id: str
    product_id: str

class ProductOut(BaseModel):
    id: str
    sku: Optional[str]
    title: Optional[str]
    last_in_stock: bool
    last_price: Optional[float]
    last_checked_at: Optional[datetime]

    class Config:
        orm_mode = True

class EventOut(BaseModel):
    id: str
    product_id: str
    event_type: str
    payload: Any
    created_at: datetime

    class Config:
        orm_mode = True
