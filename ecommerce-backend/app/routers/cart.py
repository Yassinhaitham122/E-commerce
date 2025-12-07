from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.routers.deps import current_user
from app import crud, models

router = APIRouter(prefix="/CreateOrder", tags=["cart"])

# GET: جلب الكارت للمستخدم
@router.get("/", response_model=models.Cart)
def get_cart(user=Depends(current_user), session: Session = Depends(get_session)):
    return crud.get_or_create_cart(session, user.id)

# POST: إضافة منتج للكارت
@router.post("/add", response_model=models.CartItem)
def add_to_cart(product_id: int, user=Depends(current_user), session: Session = Depends(get_session)):
    product = crud.get_product(session, product_id)
    if not product:
        raise HTTPException(404, f"Product {product_id} not found")
    return crud.add_product_to_cart(session, user.id, product_id)
