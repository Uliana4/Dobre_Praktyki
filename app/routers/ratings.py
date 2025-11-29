from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.CRUD import ratings as crud_ratings
from app.models import Rating

router = APIRouter(prefix="/ratings", tags=["ratings"])


def to_dict_rating(r: Rating) -> dict:
    return {
        "userId": r.userId,
        "movieId": r.movieId,
        "rating": r.rating,
        "timestamp": r.timestamp,
    }


@router.get("/")
def list_ratings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ratings = crud_ratings.get_ratings(db, skip=skip, limit=limit)
    return [to_dict_rating(r) for r in ratings]


@router.get("/{user_id}/{movie_id}/{timestamp}")
def read_rating(
    user_id: int,
    movie_id: int,
    timestamp: int,
    db: Session = Depends(get_db),
):
    rating = crud_ratings.get_rating(db, user_id, movie_id, timestamp)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return to_dict_rating(rating)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_rating(data: dict, db: Session = Depends(get_db)):
    """
    Przykładowe body:
    {
      "userId": 1,
      "movieId": 1,
      "rating": 4.5,
      "timestamp": 964982703
    }
    """
    rating = crud_ratings.create_rating(db, data)
    return to_dict_rating(rating)


@router.put("/{user_id}/{movie_id}/{timestamp}")
def update_rating(
    user_id: int,
    movie_id: int,
    timestamp: int,
    data: dict,
    db: Session = Depends(get_db),
):
    rating = crud_ratings.get_rating(db, user_id, movie_id, timestamp)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    rating = crud_ratings.update_rating(db, rating, data)
    return to_dict_rating(rating)


@router.delete("/{user_id}/{movie_id}/{timestamp}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_rating(
    user_id: int,
    movie_id: int,
    timestamp: int,
    db: Session = Depends(get_db),
):
    rating = crud_ratings.get_rating(db, user_id, movie_id, timestamp)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    crud_ratings.delete_rating(db, rating)
    return None