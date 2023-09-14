#!/usr/bin/python3
from functools import lru_cache
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from config import settings
from models import Base

SESSION_OPTIONS = {"autocommit": False, "autoflush": False, "expire_on_commit": False}


@lru_cache()
def get_db() -> Generator["DBEngine", None, None]:
    """Returns a database instance"""
    db: DBEngine = DBEngine()
    try:
        yield db
    finally:
        db.close()


class DBEngine:
    """Database Class"""

    def __init__(self, db_url=settings.DATABASE_URL):
        """Instantiates new database instance"""
        self.engine = create_engine(db_url, echo=settings.DEBUG_MODE)
        self.Session = scoped_session(sessionmaker(bind=self.engine, **SESSION_OPTIONS))
        if settings.TEST_MODE:
            self.drop_tables()
        self.create_tables()

    @property
    def session(self) -> Generator[scoped_session, None, None]:
        """Yields a session"""
        session: scoped_session = self.Session()
        try:
            yield session
        finally:
            session.close()

    def create_tables(self) -> None:
        """Creates new tables"""
        try:
            Base.metadata.create_all(bind=self.engine)
            print("Database tables created.")
        except SQLAlchemyError as e:
            print(f"Error creating database tables: {str(e)}")

    def drop_tables(self) -> None:
        """Drops all tables"""
        try:
            Base.metadata.drop_all(bind=self.engine)
            print("Database tables dropped.")
        except SQLAlchemyError as e:
            print(f"Error dropping database tables: {str(e)}")

    def save(self, obj: Base):
        """Saves an instance to the database"""
        session = next(self.session)
        session.add(obj)
        session.commit()

    def delete(self, obj: Base):
        """Saves an instance to the database"""
        session = next(self.session)
        session.delete(obj)
        session.commit()

    def count(self, obj: Base):
        """Returns object count in the database"""
        session = next(self.session)
        return session.query(obj).count()

    def close(self):
        """Closes the database connection"""
        session = next(self.session)
        session.close()
        self.engine.dispose()
