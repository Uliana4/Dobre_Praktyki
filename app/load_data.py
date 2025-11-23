import pandas as pd
from sqlalchemy.orm import Session
from app.database import engine
from app.models import Base, Movie, Link, Rating, Tag

# создать таблицы
Base.metadata.create_all(bind=engine)

session = Session(bind=engine)

def load_movies():
    df = pd.read_csv("data/movies.csv")
    for _, row in df.iterrows():
        session.add(Movie(
            movieId=row["movieId"],
            title=row["title"],
            genres=row["genres"]
        ))


def load_links():
    df = pd.read_csv("data/links.csv")
    for _, row in df.iterrows():
        session.add(Link(
            movieId=row["movieId"],
            imdbId=row["imdbId"],
            tmdbId=row["tmdbId"]
        ))


def load_ratings():
    df = pd.read_csv("data/ratings.csv")
    for _, row in df.iterrows():
        session.add(Rating(
            userId=row["userId"],
            movieId=row["movieId"],
            rating=row["rating"],
            timestamp=row["timestamp"]
        ))


def load_tags():
    df = pd.read_csv("data/tags.csv")
    for _, row in df.iterrows():
        session.add(Tag(
            userId=row["userId"],
            movieId=row["movieId"],
            tag=row["tag"],
            timestamp=row["timestamp"]
        ))


if __name__ == "__main__":
    load_movies()
    load_links()
    load_ratings()
    load_tags()

    session.commit()
    session.close()
    print("CSV → SQLite: DONE")

