from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Optional

class LocationBase(BaseModel):
    longitude: float
    latitude: float

    @field_validator('longitude')
    @classmethod
    def validate_longitude(cls, v: float) -> float:
        if v < -180 or v > 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v

    @field_validator('latitude')
    @classmethod
    def validate_latitude(cls, v: float) -> float:
        if v < -90 or v > 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class LocationCategoryReviewedBase(BaseModel):
    location_id: int
    category_id: int

class LocationCategoryReviewedCreate(LocationCategoryReviewedBase):
    pass

class LocationCategoryReviewed(LocationCategoryReviewedBase):
    id: int
    last_reviewed: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Recommendation(BaseModel):
    location: Location
    category: Category
    last_reviewed: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class ReviewBase(BaseModel):
    location_id: int
    category_id: int

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    last_reviewed: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)