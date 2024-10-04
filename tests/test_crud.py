import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from sqlalchemy.orm import Session
from app import crud, models
from datetime import datetime, timedelta, timezone

@pytest.fixture(scope="function")
def db():
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_get_recommendations(db: Session):
    location = models.Location(longitude=0, latitude=0)
    category = models.Category(name="Test Category")
    db.add(location)
    db.add(category)
    db.commit()

    lc1 = models.LocationCategory(location_id=location.id, category_id=category.id)
    db.add(lc1)

    lc2 = models.LocationCategory(
        location_id=location.id, 
        category_id=category.id,
        last_reviewed=datetime.now(timezone.utc) - timedelta(days=31)
    )
    db.add(lc2)

    lc3 = models.LocationCategory(
        location_id=location.id, 
        category_id=category.id,
        last_reviewed=datetime.now(timezone.utc)
    )
    db.add(lc3)

    db.commit()

    recommendations = crud.get_recommendations(db)

    assert len(recommendations) == 2
    assert recommendations[0].last_reviewed is None
    assert recommendations[1].last_reviewed is not None
    time_difference = datetime.now(timezone.utc) - recommendations[1].last_reviewed.replace(tzinfo=timezone.utc)
    assert time_difference.days > 30