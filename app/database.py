from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

def get_env_variable(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"Environment variable {var_name} is not set")
    return value

DATABASE_USERNAME = get_env_variable('DATABASE_USERNAME')
DATABASE_PASSWORD = get_env_variable('DATABASE_PASSWORD')
DATABASE_HOST = get_env_variable('DATABASE_HOST')
DATABASE_PORT = get_env_variable('DATABASE_PORT')
DATABASE_NAME = get_env_variable('DATABASE_NAME')

DATABASE_URL = f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()