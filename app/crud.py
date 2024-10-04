from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from . import models, schemas
from datetime import datetime, timedelta, timezone
from sqlalchemy import func, or_
from fastapi import HTTPException, status
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.id == location_id).first()

def get_locations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Location).offset(skip).limit(limit).all()

def create_location(db: Session, location: schemas.LocationCreate):
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
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    try:
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
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error creating category: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating category")

def create_or_update_review(db: Session, review: schemas.ReviewCreate):
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
    return db.query(models.Review).filter(models.Review.location_id == location_id, models.Review.category_id == category_id).first()

def get_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Review).offset(skip).limit(limit).all()

def get_recommendations(db: Session):
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