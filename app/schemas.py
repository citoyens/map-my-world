from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class LocationBase(BaseModel):
    """
    Base model for Location with common attributes.
    """
    longitude: float
    latitude: float

    @field_validator('longitude')
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        """
        Validate that longitude is between -180 and 180 degrees.

        Args:
            v (float): The longitude value to validate.

        Returns:
            float: The validated longitude value.

        Raises:
            ValueError: If the longitude is not between -180 and 180.
        """
        if v < -180 or v > 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v

    @field_validator('latitude')
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        """
        Validate that latitude is between -90 and 90 degrees.

        Args:
            v (float): The latitude value to validate.

        Returns:
            float: The validated latitude value.

        Raises:
            ValueError: If the latitude is not between -90 and 90.
        """
        if v < -90 or v > 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v

class LocationCreate(LocationBase):
    """
    Schema for creating a new Location. Inherits from LocationBase.
    """
    pass

class Location(LocationBase):
    """
    Schema for a complete Location, including database-specific fields.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CategoryBase(BaseModel):
    """
    Base model for Category with common attributes.
    """
    name: str

class CategoryCreate(CategoryBase):
    """
    Schema for creating a new Category. Inherits from CategoryBase.
    """
    pass

class Category(CategoryBase):
    """
    Schema for a complete Category, including database-specific fields.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LocationCategoryReviewedBase(BaseModel):
    """
    Base model for LocationCategoryReviewed with common attributes.
    """
    location_id: int
    category_id: int

class LocationCategoryReviewedCreate(LocationCategoryReviewedBase):
    """
    Schema for creating a new LocationCategoryReviewed. Inherits from LocationCategoryReviewedBase.
    """
    pass

class LocationCategoryReviewed(LocationCategoryReviewedBase):
    """
    Schema for a complete LocationCategoryReviewed, including database-specific fields.
    """
    id: int
    last_reviewed: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Recommendation(BaseModel):
    """
    Schema for a Recommendation, combining Location, Category, and review information.
    """
    location: Location
    category: Category
    last_reviewed: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class ReviewBase(BaseModel):
    """
    Base model for Review with common attributes.
    """
    location_id: int
    category_id: int

class ReviewCreate(ReviewBase):
    """
    Schema for creating a new Review. Inherits from ReviewBase.
    """
    pass

class Review(ReviewBase):
    """
    Schema for a complete Review, including database-specific fields.
    """
    id: int
    last_reviewed: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)