from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from typing import List

router = APIRouter()

@router.get("/", response_model=List[schemas.Review], status_code=status.HTTP_200_OK)
def read_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reviews = crud.get_reviews(db, skip=skip, limit=limit)
    return reviews

@router.post("/", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
def create_or_update_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_or_update_review(db=db, review=review)