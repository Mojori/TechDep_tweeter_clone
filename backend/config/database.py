from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost/tw"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
