from fastapi import FastAPI
from app.models import (
    load_movies_from_csv, load_links_from_csv, 
    load_ratings_from_csv, load_tags_from_csv
)

app = FastAPI()

movies = load_movies_from_csv("data/movies.csv")
links = load_links_from_csv("data/links.csv")
ratings = load_ratings_from_csv("data/ratings.csv")
tags = load_tags_from_csv("data/tags.csv")

# endpoint 1: hello world
@app.get("/")
def read_root():
    return {"hello": "world"}

@app.get("/movies")
def get_movies():
    return [movie.__dict__ for movie in movies]

@app.get("/links")
def get_links():
    return [l.__dict__ for l in links]

@app.get("/ratings")
def get_ratings():
    return [r.__dict__ for r in ratings]

@app.get("/tags")
def get_tags():
    return [t.__dict__ for t in tags]