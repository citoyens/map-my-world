from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class TimestampMixin:
    """
    A mixin class to add created_at and updated_at timestamps to models.
    """
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

class Location(TimestampMixin, Base):
    """
    Represents a location in the database.
    """
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    location_categories = relationship('LocationCategory', back_populates='location')
    reviews = relationship('Review', back_populates='location')

    __table_args__ = (
        Index('idx_location_coords', 'longitude', 'latitude'),
    )

class Category(TimestampMixin, Base):
    """
    Represents a category in the database.
    """
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    location_categories = relationship('LocationCategory', back_populates='category')

class Review(TimestampMixin, Base):
    """
    Represents a review in the database.
    """
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey('locations.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    last_reviewed = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    location = relationship('Location', back_populates='reviews')
    category = relationship('Category')

class LocationCategory(TimestampMixin, Base):
    """
    Represents a many-to-many relationship between locations and categories.
    """
    __tablename__ = 'location_category'
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    last_reviewed = Column(DateTime(timezone=True), default=None)
    location = relationship('Location', back_populates='location_categories')
    category = relationship('Category', back_populates='location_categories')