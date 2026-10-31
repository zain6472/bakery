from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.product import Base

DATABASE_URL = "sqlite:///./store.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


Base.metadata.create_all(bind=engine)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()