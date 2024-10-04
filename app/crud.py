from sqlite3 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import models, schemas
from datetime import datetime, timedelta, timezone
from sqlalchemy import or_
from fastapi import HTTPException, status
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_location(db: Session, location_id: int):
    """
    Retrieve a location by its ID.

    Args:
        db (Session): The database session.
        location_id (int): The ID of the location to retrieve.

    Returns:
        models.Location: The location object if found, None otherwise.
    """
    return db.query(models.Location).filter(models.Location.id == location_id).first()

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of locations with pagination.

    Args:
        db (Session): The database session.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        List[models.Location]: A list of location objects.
    """
    return db.query(models.Location).offset(skip).limit(limit).all()

def create_location(db: Session, location: schemas.LocationCreate):
    """
    Create a new location and associated location categories.

    Args:
        db (Session): The database session.
        location (schemas.LocationCreate): The location data to create.

    Returns:
        models.Location: The created location object.

    Raises:
        HTTPException: If there's an error creating the location.
    """
    try:
        db_location = models.Location(**location.dict())
        db.add(db_location)
        db.commit()
        db.refresh(db_location)

        categories = db.query(models.Category).all()
        db_location_categories = [
            models.LocationCategory(location_id=db_location.id, category_id=category.id)
            for category in categories
        ]
        db.bulk_save_objects(db_location_categories)
        db.commit()

        return db_location
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating location: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating location")

def get_category(db: Session, category_id: int):
    """
    Retrieve a category by its ID.

    Args:
        db (Session): The database session.
        category_id (int): The ID of the category to retrieve.

    Returns:
        models.Category: The category object if found, None otherwise.
    """
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of categories with pagination.

    Args:
        db (Session): The database session.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        List[models.Category]: A list of category objects.
    """
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    """
    Create a new category or return existing if it already exists.

    Args:
        db (Session): The database session.
        category (schemas.CategoryCreate): The category data to create.

    Returns:
        models.Category: The created or existing category object.

    Raises:
        HTTPException: If there's an error creating the category.
    """
    try:
        existing_category = db.query(models.Category).filter(models.Category.name == category.name).first()
        if existing_category:
            logger.info(f"Category '{category.name}' already exists. Returning existing category.")
            return existing_category

        db_category = models.Category(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)

        locations = db.query(models.Location).all()
        db_location_categories = [
            models.LocationCategory(location_id=location.id, category_id=db_category.id)
            for location in locations
        ]
        db.bulk_save_objects(db_location_categories)
        db.commit()

        return db_category
    except IntegrityError as e:
        db.rollback()
        logger.error(f"IntegrityError creating category: {str(e)}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating category: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating category")
    
def create_or_update_review(db: Session, review: schemas.ReviewCreate):
    """
    Create a new review or update an existing one.

    Args:
        db (Session): The database session.
        review (schemas.ReviewCreate): The review data to create or update.

    Returns:
        models.Review: The created or updated review object.

    Raises:
        HTTPException: If there's an error creating or updating the review.
    """
    try:
        now = datetime.now(timezone.utc)
        db_review = db.query(models.Review).filter(
            models.Review.location_id == review.location_id,
            models.Review.category_id == review.category_id
        ).first()

        if db_review:
            db_review.last_reviewed = now
        else:
            db_review = models.Review(
                location_id=review.location_id,
                category_id=review.category_id,
                last_reviewed=now
            )
            db.add(db_review)

        db_location_category = db.query(models.LocationCategory).filter(
            models.LocationCategory.location_id == review.location_id,
            models.LocationCategory.category_id == review.category_id
        ).first()

        if db_location_category:
            db_location_category.last_reviewed = now
        else:
            db_location_category = models.LocationCategory(
                location_id=review.location_id,
                category_id=review.category_id,
                last_reviewed=now
            )
            db.add(db_location_category)

        db.commit()
        db.refresh(db_review)
        
        return db_review
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating or updating review: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating or updating review")

def get_review(db: Session, location_id: int, category_id: int):
    """
    Retrieve a review by location and category IDs.

    Args:
        db (Session): The database session.
        location_id (int): The ID of the location.
        category_id (int): The ID of the category.

    Returns:
        models.Review: The review object if found, None otherwise.
    """
    return db.query(models.Review).filter(models.Review.location_id == location_id, models.Review.category_id == category_id).first()

def get_reviews(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of reviews with pagination.

    Args:
        db (Session): The database session.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        List[models.Review]: A list of review objects.
    """
    return db.query(models.Review).offset(skip).limit(limit).all()

def get_recommendations(db: Session):
    """
    Retrieve a list of recommendations based on review history.

    This function returns a list of location-category combinations that have not been
    reviewed in the last 30 days, prioritizing those that have never been reviewed.

    Args:
        db (Session): The database session.

    Returns:
        List[schemas.Recommendation]: A list of recommendation objects.

    Raises:
        HTTPException: If there's an error retrieving recommendations.
    """
    try:
        current_time = datetime.now(timezone.utc)
        threshold_date = current_time - timedelta(days=30)

        recommendations = db.query(
            models.Location,
            models.Category,
            models.LocationCategory.last_reviewed
        ).select_from(models.LocationCategory).join(
            models.Location,
            models.LocationCategory.location_id == models.Location.id
        ).join(
            models.Category,
            models.LocationCategory.category_id == models.Category.id
        ).filter(
            or_(
                models.LocationCategory.last_reviewed.is_(None),
                models.LocationCategory.last_reviewed < threshold_date
            )
        ).order_by(
            models.LocationCategory.last_reviewed.is_(None).desc(),
            models.LocationCategory.last_reviewed.asc()
        ).limit(10).all()

        logger.info(f"Number of recommendations retrieved: {len(recommendations)}")

        return [
            schemas.Recommendation(
                location=recommendation[0],
                category=recommendation[1],
                last_reviewed=recommendation[2]
            )
            for recommendation in recommendations
        ]
    except SQLAlchemyError as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error getting recommendations")