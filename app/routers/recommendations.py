from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Recommendation], status_code=status.HTTP_200_OK)
def get_recommendations(db: Session = Depends(get_db)):
    """
    Retrieve a list of recommendations.

    This endpoint returns a list of 10 location-category combinations that have not been
    reviewed in the last 30 days, prioritizing those that have never been reviewed.

    Args:
        db (Session): The database session.

    Returns:
        List[schemas.Recommendation]: A list of recommended location-category combinations.
    """
    return crud.get_recommendations(db)