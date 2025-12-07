from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List, Optional
from app.database import get_session
from app import crud, models
from app.schemas import ProductCreate, ProductRead
from app.routers.auth import current_user


router = APIRouter(prefix="/products", tags=["products"])

# ----------------- LIST PRODUCTS -----------------
@router.get("/", response_model=List[ProductRead])
def list_products(
    skip: int = 0,
    limit: int = 100,
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    min_stock: Optional[int] = Query(None),
    max_stock: Optional[int] = Query(None),
    name: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    return crud.get_products(
        session=session,
        skip=skip,
        limit=limit,
        min_price=min_price,
        max_price=max_price,
        min_stock=min_stock,
        max_stock=max_stock,
        name=name
    )

# ----------------- CREATE PRODUCT -----------------
@router.post("/", response_model=ProductRead)
def create_product(
    item: ProductCreate,
    session: Session = Depends(get_session),
    user: models.User = Depends(current_user),
):
    product = models.Product(**item.dict())
    return crud.create_product(session, product)
