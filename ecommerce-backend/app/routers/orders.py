from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.routers.deps import current_user
from app.schemas import OrderCreate, OrderItemCreate
from app import crud, models


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", status_code=201)
def create_order(order_in: OrderCreate, session: Session = Depends(get_session), user = Depends(current_user)):
    # حساب سعر بسيط
    total = 0.0
    for it in order_in.items:
        product = crud.get_product(session, it.product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {it.product_id} not found")
        if product.stock < it.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.id}")
        total += product.price * it.quantity
        # قلل المخزون
        product.stock -= it.quantity
        session.add(product)
    session.commit()

    order = crud.create_order(session, user.id, total)
    for it in order_in.items:
        oi = models.OrderItem(order_id=order.id, product_id=it.product_id, quantity=it.quantity)
        crud.create_order_item(session, oi)

    return {"order_id": order.id, "total_price": total}