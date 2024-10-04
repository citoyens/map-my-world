from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the DATABASE_URL from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Convert postgres:// to postgresql:// if necessary
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class
Base = declarative_base()

def get_db():
    """
    Dependency function to get a database session.

    Yields:
        Session: A SQLAlchemy Session object.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()