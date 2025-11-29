from sqlalchemy.orm import Session
from app.models import Movie


def get_movie(db: Session, movie_id: int) -> Movie | None:
    return db.query(Movie).filter(Movie.movieId == movie_id).first()


def get_movies(db: Session, skip: int = 0, limit: int = 100) -> list[Movie]:
    return db.query(Movie).offset(skip).limit(limit).all()


def create_movie(db: Session, data: dict) -> Movie:
    """
    data może zawierać np.:
    {
        "title": "Nazwa filmu",
        "genres": "Action|Comedy",
        # opcjonalnie "movieId": 123
    }
    """
    movie = Movie(**data)
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


def update_movie(db: Session, movie: Movie, data: dict) -> Movie:
    """
    Aktualizuje przekazany obiekt Movie danymi ze słownika data.
    """
    # opcjonalnie można pominąć movieId, jeśli nie chcesz go zmieniać
    for key, value in data.items():
        if key == "movieId":
            continue
        if hasattr(movie, key):
            setattr(movie, key, value)

    db.commit()
    db.refresh(movie)
    return movie


def delete_movie(db: Session, movie: Movie) -> None:
    db.delete(movie)
    db.commit()