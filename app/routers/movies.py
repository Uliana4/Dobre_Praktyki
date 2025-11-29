from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.CRUD import movies as crud_movies
from app.models import Movie

router = APIRouter(prefix="/movies", tags=["movies"])


def to_dict_movie(movie: Movie) -> dict:
    return {
        "movieId": movie.movieId,
        "title": movie.title,
        "genres": movie.genres,
    }


@router.get("/")
def list_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = crud_movies.get_movies(db, skip=skip, limit=limit)
    return [to_dict_movie(m) for m in movies]


@router.get("/{movie_id}")
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = crud_movies.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return to_dict_movie(movie)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_movie(data: dict, db: Session = Depends(get_db)):
    """
    Przykładowe body:
    {
      "title": "Toy Story (1995)",
      "genres": "Adventure|Animation|Children|Comedy|Fantasy"
    }
    """
    movie = crud_movies.create_movie(db, data)
    return to_dict_movie(movie)


@router.put("/{movie_id}")
def update_movie(movie_id: int, data: dict, db: Session = Depends(get_db)):
    movie = crud_movies.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie = crud_movies.update_movie(db, movie, data)
    return to_dict_movie(movie)


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = crud_movies.get_movie(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    crud_movies.delete_movie(db, movie)
    return None