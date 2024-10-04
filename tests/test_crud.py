import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from sqlalchemy.orm import Session
from app import crud, models
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
import time
import psycopg2

load_dotenv('.env.test')

def wait_for_db(max_retries=30, delay_seconds=1):
    retries = 0
    while retries < max_retries:
        try:
            conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            conn.close()
            print("Database is ready!")
            return
        except psycopg2.OperationalError:
            retries += 1
            print(f"Waiting for database... (Attempt {retries}/{max_retries})")
            time.sleep(delay_seconds)
    raise Exception("Could not connect to the database")

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    wait_for_db()
    DATABASE_URL = os.getenv('DATABASE_URL')
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    DATABASE_URL = os.getenv('DATABASE_URL')
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    engine = create_engine(DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

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