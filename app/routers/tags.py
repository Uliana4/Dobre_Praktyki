from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.CRUD import tags as crud_tags
from app.models import Tag

router = APIRouter(prefix="/tags", tags=["tags"])


def to_dict_tag(t: Tag) -> dict:
    return {
        "userId": t.userId,
        "movieId": t.movieId,
        "tag": t.tag,
        "timestamp": t.timestamp,
    }


@router.get("/")
def list_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = crud_tags.get_tags(db, skip=skip, limit=limit)
    return [to_dict_tag(t) for t in tags]


@router.get("/{user_id}/{movie_id}/{tag}/{timestamp}")
def read_tag(
    user_id: int,
    movie_id: int,
    tag: str,
    timestamp: int,
    db: Session = Depends(get_db),
):
    tag_obj = crud_tags.get_tag(db, user_id, movie_id, tag, timestamp)
    if not tag_obj:
        raise HTTPException(status_code=404, detail="Tag not found")
    return to_dict_tag(tag_obj)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_tag(data: dict, db: Session = Depends(get_db)):
    """
    Przykładowe body:
    {
      "userId": 1,
      "movieId": 1,
      "tag": "funny",
      "timestamp": 964982703
    }
    """
    tag_obj = crud_tags.create_tag(db, data)
    return to_dict_tag(tag_obj)


@router.put("/{user_id}/{movie_id}/{tag}/{timestamp}")
def update_tag(
    user_id: int,
    movie_id: int,
    tag: str,
    timestamp: int,
    data: dict,
    db: Session = Depends(get_db),
):
    tag_obj = crud_tags.get_tag(db, user_id, movie_id, tag, timestamp)
    if not tag_obj:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag_obj = crud_tags.update_tag(db, tag_obj, data)
    return to_dict_tag(tag_obj)


@router.delete("/{user_id}/{movie_id}/{tag}/{timestamp}",
               status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    user_id: int,
    movie_id: int,
    tag: str,
    timestamp: int,
    db: Session = Depends(get_db),
):
    tag_obj = crud_tags.get_tag(db, user_id, movie_id, tag, timestamp)
    if not tag_obj:
        raise HTTPException(status_code=404, detail="Tag not found")
    crud_tags.delete_tag(db, tag_obj)
    return None