from sqlalchemy.orm import Session
from app.models import Tag

def get_tag(
    db: Session,
    user_id: int,
    movie_id: int,
    tag: str,
    timestamp: int,
) -> Tag | None:
    return (
        db.query(Tag)
        .filter(
            Tag.userId == user_id,
            Tag.movieId == movie_id,
            Tag.tag == tag,
            Tag.timestamp == timestamp,
        )
        .first()
    )


def get_tags(db: Session, skip: int = 0, limit: int = 100) -> list[Tag]:
    return db.query(Tag).offset(skip).limit(limit).all()


def create_tag(db: Session, data: dict) -> Tag:
    """
    data może zawierać np.:
    {
        "userId": 1,
        "movieId": 10,
        "tag": "funny",
        "timestamp": 1234567890
    }
    """
    tag_obj = Tag(**data)
    db.add(tag_obj)
    db.commit()
    db.refresh(tag_obj)
    return tag_obj


def update_tag(db: Session, tag_obj: Tag, data: dict) -> Tag:
    """
    Można np. pozwolić zmieniać sam tekst 'tag',
    ale zostawiamy elastyczną wersję.
    """
    for key, value in data.items():
        # PK: userId, movieId, tag, timestamp – nie ruszamy
        if key in ("userId", "movieId", "tag", "timestamp"):
            continue
        if hasattr(tag_obj, key):
            setattr(tag_obj, key, value)

    db.commit()
    db.refresh(tag_obj)
    return tag_obj


def delete_tag(db: Session, tag_obj: Tag) -> None:
    db.delete(tag_obj)
    db.commit()