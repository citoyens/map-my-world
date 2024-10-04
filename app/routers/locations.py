from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Location, status_code=status.HTTP_201_CREATED)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    """
    Create a new location.
    
    This endpoint allows you to create a new location in the database.

    Parameters:
    - **location**: A LocationCreate object containing the longitude and latitude of the new location.

    Returns:
    - A Location object with the details of the created location, including its ID and timestamps.

    Raises:
    - 500 Internal Server Error: If there's an unexpected error during location creation.
    """
    return crud.create_location(db=db, location=location)

@router.get("/", response_model=List[schemas.Location])
def read_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of locations.
    
    This endpoint returns a paginated list of all locations in the database.

    Parameters:
    - **skip**: Number of locations to skip (default: 0)
    - **limit**: Maximum number of locations to return (default: 100)

    Returns:
    - A list of Location objects, each containing the location's details.
    """
    locations = crud.get_locations(db, skip=skip, limit=limit)
    return locations

@router.get("/{location_id}", response_model=schemas.Location)
def read_location(location_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific location by ID.
    
    This endpoint returns the details of a specific location identified by its ID.

    Parameters:
    - **location_id**: The ID of the location to retrieve (path parameter)

    Returns:
    - A Location object containing the details of the requested location.

    Raises:
    - 404 Not Found: If no location with the given ID exists.
    """
    db_location = crud.get_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return db_location