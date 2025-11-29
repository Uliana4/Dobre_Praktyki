from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.CRUD import links as crud_links
from app.models import Link

router = APIRouter(prefix="/links", tags=["links"])


def to_dict_link(link: Link) -> dict:
    return {
        "movieId": link.movieId,
        "imdbId": link.imdbId,
        "tmdbId": link.tmdbId,
    }


@router.get("/")
def list_links(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    links = crud_links.get_links(db, skip=skip, limit=limit)
    return [to_dict_link(l) for l in links]


@router.get("/{movie_id}")
def read_link(movie_id: int, db: Session = Depends(get_db)):
    link = crud_links.get_link(db, movie_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return to_dict_link(link)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_link(data: dict, db: Session = Depends(get_db)):
    """
    Przykładowe body:
    {
      "movieId": 1,
      "imdbId": 114709,
      "tmdbId": 862
    }
    """
    link = crud_links.create_link(db, data)
    return to_dict_link(link)


@router.put("/{movie_id}")
def update_link(movie_id: int, data: dict, db: Session = Depends(get_db)):
    link = crud_links.get_link(db, movie_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    link = crud_links.update_link(db, link, data)
    return to_dict_link(link)


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(movie_id: int, db: Session = Depends(get_db)):
    link = crud_links.get_link(db, movie_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    crud_links.delete_link(db, link)
    return None