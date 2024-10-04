from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Recommendation], status_code=status.HTTP_200_OK)
def get_recommendations(db: Session = Depends(get_db)):
    return crud.get_recommendations(db)