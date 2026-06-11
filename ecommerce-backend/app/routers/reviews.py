from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select
from typing import List, Optional
from app.database import get_session
from app import crud, models
from app.schemas import ReviewCreate,ReviewRead
from app.routers.deps import current_user

router = APIRouter(prefix="/reviews",tags=["reviews"])

#POST /reviews/

@router.post("/",response_model=ReviewRead)
def create_review(
  item: ReviewCreate,
  session: Session = Depends(get_session),
  user: models.User = Depends(current_user)  
):
    reviews = models.Review(**item.dict(),user_id=user.id)
    return crud.create_review(session,reviews)
    
    
#GET /reviews/{product_id}    


@router.get("/{product_id}", response_model=List[ReviewRead])
def list_reviews(
  product_id: int,  
  session: Session = Depends(get_session),
  
):
    return crud.get_product_reviews(session=session, product_id=product_id)
    