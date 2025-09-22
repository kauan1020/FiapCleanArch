from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time


def get_database_url():
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        return database_url

    db_user = os.getenv('DB_USER', 'admin')
    db_password = os.getenv('DB_PASSWORD', 'password')
    db_host = os.getenv('DB_HOST', 'db')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'vehicle_store')

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def create_engine_with_retry(max_retries=5, retry_delay=5):
    database_url = get_database_url()

    for attempt in range(max_retries):
        try:
            engine = create_engine(database_url)
            engine.connect().close()
            return engine
        except Exception as e:
            print(f"Database connection attempt {attempt + 1} failed: {e}. Retrying in {retry_delay} seconds...")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise e


engine = create_engine_with_retry()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()