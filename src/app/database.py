from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from .config import settings

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    pass


def db_dependency() -> Session:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
