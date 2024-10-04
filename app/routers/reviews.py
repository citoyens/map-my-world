from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from typing import List

router = APIRouter()

@router.get("/", response_model=List[schemas.Review], status_code=status.HTTP_200_OK)
def read_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve a list of reviews.

    Args:
        skip (int): Number of reviews to skip (for pagination).
        limit (int): Maximum number of reviews to return.
        db (Session): The database session.

    Returns:
        List[schemas.Review]: A list of reviews.
    """
    reviews = crud.get_reviews(db, skip=skip, limit=limit)
    return reviews

@router.post("/", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
def create_or_update_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    """
    Create a new review or update an existing one.

    If a review for the given location-category combination already exists,
    it will be updated. Otherwise, a new review will be created.

    Args:
        review (schemas.ReviewCreate): The review data to create or update.
        db (Session): The database session.

    Returns:
        schemas.Review: The created or updated review.
    """
    return crud.create_or_update_review(db=db, review=review)