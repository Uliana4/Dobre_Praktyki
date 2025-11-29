from sqlalchemy.orm import Session
from app.models import Link


def get_link(db: Session, movie_id: int) -> Link | None:
    return db.query(Link).filter(Link.movieId == movie_id).first()


def get_links(db: Session, skip: int = 0, limit: int = 100) -> list[Link]:
    return db.query(Link).offset(skip).limit(limit).all()


def create_link(db: Session, data: dict) -> Link:
    """
    data może zawierać np.:
    {
        "movieId": 1,
        "imdbId": 12345,
        "tmdbId": 67890
    }
    """
    link = Link(**data)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def update_link(db: Session, link: Link, data: dict) -> Link:
    for key, value in data.items():
        # movieId jest PK – zwykle nie zmieniamy
        if key == "movieId":
            continue
        if hasattr(link, key):
            setattr(link, key, value)

    db.commit()
    db.refresh(link)
    return link


def delete_link(db: Session, link: Link) -> None:
    db.delete(link)
    db.commit()