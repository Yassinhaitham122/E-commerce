from app import crud, models
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

# database في الـ RAM بس للـ testing
def get_test_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
        
       
def test_create_product():
    session = next(get_test_session())
    
    product = models.Product(name="Test Product", price=100.0, stock=10)
    result = crud.create_product(session, product)
    
    assert result.id is not None
    assert result.name == "Test Product"
    assert result.price == 100.0        
    
def test_get_product():
    session =  next(get_test_session())
    product = models.Product(name="Test Product",price=50, stock=+1)
    result = crud.create_product(session, product)
    products = crud.get_products(session)
    
    assert result.stock != 0
    assert len(products) > 0
    
    
def test_create_order():    
    session = next(get_test_session())
    user = models.User(name= "testUser",email="test@test.com", password_hash="123")
    session.add(user)
    session.commit()
    session.refresh(user)
    result = crud.create_order(session,user_id=user.id,total_price=10.0) 
    
    assert result.user_id 
    assert result.total_price >= 10          
    
def test_create_review():
    session = next(get_test_session())
    
    # عمل user
    user = models.User(name="testUser", email="test@test.com", password_hash="123")
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # عمل product
    product = models.Product(name="Test Product", price=50.0, stock=1)
    session.add(product)
    session.commit()
    session.refresh(product)
    
    # عمل review مربوط بيهم
    review = models.Review(user_id=user.id, product_id=product.id, rating=5, comment="great!")
    result = crud.create_review(session, review)
    
    assert result.id is not None
    assert result.rating == 5
    assert result.user_id == user.id
    
    

    
    
    