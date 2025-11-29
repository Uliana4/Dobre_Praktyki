import csv
from sqlalchemy.orm import Session

from app.models import get_engine, Movie, Link, Rating, Tag


def load_movies(session: Session, csv_path: str = "data/movies.csv"):
    print("Ładowanie filmów...")
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        movies = [
            Movie(
                movieId=int(row["movieId"]),
                title=row["title"],
                genres=row["genres"],
            )
            for row in reader
        ]
    session.bulk_save_objects(movies)
    session.commit()
    print("Załadowano filmów:", len(movies))


def load_links(session: Session, csv_path: str = "data/links.csv"):
    print("Ładowanie linków...")
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        links = []
        for row in reader:
            imdb = int(row["imdbId"]) if row["imdbId"] else None
            tmdb = int(row["tmdbId"]) if row["tmdbId"] else None

            links.append(
                Link(
                    movieId=int(row["movieId"]),
                    imdbId=imdb,
                    tmdbId=tmdb,
                )
            )

    session.bulk_save_objects(links)
    session.commit()
    print("Załadowano linków:", len(links))


def load_ratings(session: Session, csv_path: str = "data/ratings.csv"):
    print("Ładowanie ocen...")
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        batch = []
        count = 0

        for row in reader:
            batch.append(
                Rating(
                    userId=int(row["userId"]),
                    movieId=int(row["movieId"]),
                    rating=float(row["rating"]),
                    timestamp=int(row["timestamp"]),
                )
            )

            if len(batch) >= 10000:
                session.bulk_save_objects(batch)
                session.commit()
                count += len(batch)
                print("Załadowano ocen:", count)
                batch = []

        if batch:
            session.bulk_save_objects(batch)
            session.commit()
            count += len(batch)

    print("Łącznie załadowano ocen:", count)


def load_tags(session: Session, csv_path: str = "data/tags.csv"):
    print("Ładowanie tagów...")
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        tags = [
            Tag(
                userId=int(row["userId"]),
                movieId=int(row["movieId"]),
                tag=row["tag"],
                timestamp=int(row["timestamp"]),
            )
            for row in reader
        ]

    session.bulk_save_objects(tags)
    session.commit()
    print("Załadowano tagów:", len(tags))


def main():
    engine = get_engine("movies.db")

    with Session(engine) as session:
        load_movies(session)
        load_links(session)
        load_ratings(session)
        load_tags(session)

    print("Załadowano wszystkie dane do bazy")


if __name__ == "__main__":
    main()