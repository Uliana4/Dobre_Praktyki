from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Movie, Link, Rating, Tag

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return [{"movieId": m.movieId, "title": m.title, "genres": m.genres} for m in movies]


@app.get("/links")
def get_links(db: Session = Depends(get_db)):
    links = db.query(Link).all()
    return [{"movieId": l.movieId, "imdbId": l.imdbId, "tmdbId": l.tmdbId} for l in links]


@app.get("/ratings")
def get_ratings(db: Session = Depends(get_db)):
    ratings = db.query(Rating).all()
    return [{"userId": r.userId, "movieId": r.movieId, "rating": r.rating} for r in ratings]


@app.get("/tags")
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return [{"userId": t.userId, "movieId": t.movieId, "tag": t.tag} for t in tags]
