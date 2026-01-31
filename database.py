from sqlalchemy import create_engine, Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///app.db"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    movieId = Column(Integer, primary_key=True)
    title = Column(String)
    genres = Column(String)

class Link(Base):
    __tablename__ = "links"
    movieId = Column(Integer, primary_key=True)
    imdbId = Column(String)
    tmdbId = Column(String)

class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer)
    movieId = Column(Integer)
    rating = Column(Float)
    timestamp = Column(Integer)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, autoincrement=True)
    userId = Column(Integer)
    movieId = Column(Integer)
    tag = Column(String)
    timestamp = Column(Integer)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    roles = Column(JSON, default=list)  # List of roles, e.g., ["ROLE_USER", "ROLE_ADMIN"]

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)