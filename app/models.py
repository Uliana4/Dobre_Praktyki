from __future__ import annotations  # ważne dla forward refs typu "Rating"

from sqlalchemy import create_engine, Integer, String, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.schema import PrimaryKeyConstraint


class Base(DeclarativeBase):
    """Bazowa klasa dla modeli ORM."""
    pass


def get_engine(db_path: str = "movies.db"):
    """Zwraca silnik SQLAlchemy do bazy SQLite."""
    return create_engine(f"sqlite:///{db_path}", echo=False)


class Movie(Base):
    __tablename__ = "movies"

    movieId: Mapped[int] = mapped_column(Integer, primary_key=True)
    title:   Mapped[str] = mapped_column(String, nullable=False)
    genres:  Mapped[str] = mapped_column(String, nullable=False)

    # relacje – UWAGA: bez "| None" poza Mapped
    links:   Mapped["Link"] = relationship(back_populates="movie", uselist=False)
    ratings: Mapped[list["Rating"]] = relationship(back_populates="movie")
    tags:    Mapped[list["Tag"]] = relationship(back_populates="movie")


class Link(Base):
    __tablename__ = "links"

    movieId: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("movies.movieId"),
        primary_key=True,
    )
    imdbId: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tmdbId: Mapped[int | None] = mapped_column(Integer, nullable=True)

    movie: Mapped[Movie] = relationship(back_populates="links")


class Rating(Base):
    __tablename__ = "ratings"

    userId:    Mapped[int]   = mapped_column(Integer, nullable=False)
    movieId:   Mapped[int]   = mapped_column(
        Integer,
        ForeignKey("movies.movieId"),
        nullable=False,
    )
    rating:    Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[int]   = mapped_column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("userId", "movieId", "timestamp"),
    )

    movie: Mapped[Movie] = relationship(back_populates="ratings")


class Tag(Base):
    __tablename__ = "tags"

    userId:    Mapped[int] = mapped_column(Integer, nullable=False)
    movieId:   Mapped[int] = mapped_column(
        Integer,
        ForeignKey("movies.movieId"),
        nullable=False,
    )
    tag:       Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("userId", "movieId", "tag", "timestamp"),
    )

    movie: Mapped[Movie] = relationship(back_populates="tags")