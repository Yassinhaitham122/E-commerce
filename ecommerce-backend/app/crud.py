from typing import List, Optional
from sqlmodel import Session, select
from app import models

# ==========================
# USERS
# ==========================
def get_user_by_id(session: Session, user_id: int) -> Optional[models.User]:
    return session.get(models.User, user_id)

def get_user_by_email(session: Session, email: str) -> Optional[models.User]:
    return session.exec(
        select(models.User).where(models.User.email == email)
    ).first()

def list_users(session: Session, skip: int = 0, limit: int = 50) -> List[models.User]:
    return session.exec(
        select(models.User).offset(skip).limit(limit)
    ).all()

def create_user(session: Session, name: str, email: str, password_hash: str) -> models.User:
    user = models.User(name=name, email=email, password_hash=password_hash)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_user(session: Session, user_id: int, name: Optional[str] = None) -> Optional[models.User]:
    user = session.get(models.User, user_id)
    if not user:
        return None
    if name is not None:
        user.name = name
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(models.User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True

# ==========================
# PRODUCTS
# ==========================
def create_product(session: Session, product: models.Product) -> models.Product:
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

def get_products(session: Session, skip: int = 0, limit: int = 100,
                 min_price: Optional[float] = None,
                 max_price: Optional[float] = None,
                 min_stock: Optional[int] = None,
                 max_stock: Optional[int] = None,
                 name: Optional[str] = None) -> List[models.Product]:
    query = select(models.Product)
    if min_price is not None:
        query = query.where(models.Product.price >= min_price)
    if max_price is not None:
        query = query.where(models.Product.price <= max_price)
    if min_stock is not None:
        query = query.where(models.Product.stock >= min_stock)
    if max_stock is not None:
        query = query.where(models.Product.stock <= max_stock)
    if name:
        query = query.where(models.Product.name.ilike(f"%{name}%"))
    return session.exec(query.offset(skip).limit(limit)).all()

def get_product(session: Session, product_id: int) -> Optional[models.Product]:
    return session.get(models.Product, product_id)

# ==========================
# CART / CARTITEM
# ==========================
def get_or_create_cart(session: Session, user_id: int) -> models.Cart:
    cart = session.exec(select(models.Cart).where(models.Cart.user_id == user_id)).first()
    if not cart:
        cart = models.Cart(user_id=user_id)
        session.add(cart)
        session.commit()
        session.refresh(cart)
    return cart

def add_product_to_cart(session: Session, user_id: int, product_id: int):
    cart = get_or_create_cart(session, user_id)
    item = session.exec(
        select(models.CartItem).where(models.CartItem.cart_id == cart.id,
                                       models.CartItem.product_id == product_id)
    ).first()
    if item:
        item.quantity += 1
    else:
        item = models.CartItem(cart_id=cart.id, product_id=product_id, quantity=1)
        session.add(item)
    session.commit()
    session.refresh(item)
    return item

def view_cart(session: Session, user_id: int):
    cart = get_or_create_cart(session, user_id)
    return cart.items

# ==========================
# ORDERS
# ==========================
def create_order(session: Session, user_id: int, total_price: float) -> models.Order:
    order = models.Order(user_id=user_id, total_price=total_price)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def create_order_item(session: Session, order_item: models.OrderItem) -> models.OrderItem:
    session.add(order_item)
    session.commit()
    session.refresh(order_item)
    return order_item

def create_order_from_cart(session: Session, user_id: int) -> models.Order:
    cart = get_or_create_cart(session, user_id)
    total_price = sum(item.product.price * item.quantity for item in cart.items)

    order = models.Order(user_id=user_id, total_price=total_price)
    session.add(order)
    session.commit()
    session.refresh(order)

    for item in cart.items:
        order_item = models.OrderItem(order_id=order.id, product_id=item.product_id, quantity=item.quantity)
        session.add(order_item)
        # تقليل المخزون
        item.product.stock -= item.quantity
        session.add(item.product)

    # مسح محتويات الكارت بعد التحويل
    for item in cart.items:
        session.delete(item)

    session.commit()
    session.refresh(order)
    return order
