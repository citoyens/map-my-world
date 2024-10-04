from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new category.

    This endpoint allows you to create a new category in the database.

    Parameters:
    - **category**: A CategoryCreate object containing the name of the new category.

    Returns:
    - A Category object with the details of the created category, including its ID and timestamps.

    Raises:
    - 409 Conflict: If a category with the same name already exists.
    - 500 Internal Server Error: If there's an unexpected error during category creation.
    """
    return crud.create_category(db=db, category=category)

@router.get("/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of categories.

    This endpoint returns a paginated list of all categories in the database.

    Parameters:
    - **skip**: Number of categories to skip (default: 0)
    - **limit**: Maximum number of categories to return (default: 100)

    Returns:
    - A list of Category objects, each containing the category's details.
    """
    categories = crud.get_categories(db=db, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific category by ID.

    This endpoint returns the details of a specific category identified by its ID.

    Parameters:
    - **category_id**: The ID of the category to retrieve (path parameter)

    Returns:
    - A Category object containing the details of the requested category.

    Raises:
    - 404 Not Found: If no category with the given ID exists.
    """
    db_category = crud.get_category(db=db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Category not found")
    return db_category