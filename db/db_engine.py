#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from models.base_model import Base, BaseModel
from utils.settings import get_settings
from typing import Generator

settings = get_settings()

DATABASE_URL = 'postgresql+psycopg2://{0}:{1}@{2}:5432/{3}'.\
                    format(settings.DB_USERNAME, settings.DB_PASSWORD, settings.DB_HOST, settings.DB_NAME)


SESSION_OPTIONS = {
    "autocommit": False, 
    'autoflush': False,
    'expire_on_commit': False
}

class DBEngine:
    """Database Class"""

    def __init__(self, db_url=DATABASE_URL):
        """Instantiates new database instance"""
        self.engine = create_engine(db_url, echo=settings.DEBUG_MODE)
        self.Session = scoped_session(sessionmaker(bind=self.engine, **SESSION_OPTIONS))
        if settings.TEST_MODE:
            self.drop_tables()

    @property
    def session(self) -> Generator[scoped_session, None, None]:
        """Yields a session"""
        session: scoped_session = self.Session()
        try:
            yield session
        finally: 
            session.close()

    def reload(self) -> None:
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

    def save(self, obj: BaseModel):
        """Saves an instance to the database"""
        session = next(self.session)
        session.add(obj)
        session.commit()
    
    def delete(self, obj: BaseModel):
        """Saves an instance to the database"""
        session = next(self.session)
        session.delete(obj)
        session.commit()
    
    def count(self, obj: BaseModel):
        """Returns object count in the database"""
        session = next(self.session)
        return session.query(obj).count()



