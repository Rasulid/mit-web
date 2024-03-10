from sys import modules

import psycopg2
from sqlalchemy import NullPool, create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings, SYNC_DATABASE_URI, SYNC_TEST_DATABASE_URI


def create_test_db():
    conn = psycopg2.connect(
        host=settings.DATABASE_HOST,
        password=settings.DATABASE_PASSWORD,
        database='template1',
        user='postgres'
    )
    conn.fetch(f"DROP TABLE IF EXISTS {settings.TEST_DATABASE}")
    conn.fetch(f"CREATE DATABASE {settings.TEST_DATABASE}")
    conn.close()


DATABASE_URL = SYNC_DATABASE_URI
if "pytest" in modules:
    DATABASE_URL = SYNC_TEST_DATABASE_URI


engin = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    poolclass=NullPool
)

if "pytest" in modules:
    create_test_db()


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engin,
    expire_on_commit=False
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
