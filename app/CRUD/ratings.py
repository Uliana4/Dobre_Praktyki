from sqlalchemy.orm import Session
from app.models import Rating


def get_rating(
    db: Session,
    user_id: int,
    movie_id: int,
    timestamp: int,
) -> Rating | None:
    return (
        db.query(Rating)
        .filter(
            Rating.userId == user_id,
            Rating.movieId == movie_id,
            Rating.timestamp == timestamp,
        )
        .first()
    )


def get_ratings(db: Session, skip: int = 0, limit: int = 100) -> list[Rating]:
    return db.query(Rating).offset(skip).limit(limit).all()


def create_rating(db: Session, data: dict) -> Rating:
    """
    data może zawierać np.:
    {
        "userId": 1,
        "movieId": 10,
        "rating": 4.5,
        "timestamp": 1234567890
    }
    """
    rating = Rating(**data)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


def update_rating(db: Session, rating: Rating, data: dict) -> Rating:
    """
    Zwykle sens ma zmiana pola 'rating',
    ale zostawiamy to elastyczne.
    """
    for key, value in data.items():
        # PK: userId, movieId, timestamp – zwykle nie zmieniamy
        if key in ("userId", "movieId", "timestamp"):
            continue
        if hasattr(rating, key):
            setattr(rating, key, value)

    db.commit()
    db.refresh(rating)
    return rating


def delete_rating(db: Session, rating: Rating) -> None:
    db.delete(rating)
    db.commit()