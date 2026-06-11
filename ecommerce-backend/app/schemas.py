from datetime import datetime

from pydantic import BaseModel, EmailStr
from typing import Optional, List


# ==========================
# USERS
# ==========================

class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str | None = None


# ==========================
# AUTH
# ==========================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ==========================
# PRODUCTS
# ==========================

class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    stock: int


class ProductRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int

    class Config:
        orm_mode = True


# ==========================
# ORDERS
# ==========================

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

###########  Reviews #############

class ReviewCreate(BaseModel):
    product_id: int
    rating: int
    comment: Optional[str] = None



class ReviewRead(BaseModel):
    id: int
    user_id: int
    product_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True