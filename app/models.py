import csv
from typing import List

class Movie:
    def __init__(self, movieId: int, title: str, genres: str):
        self.movieId = movieId
        self.title = title
        self.genres = genres

    def to_dict(self):
        return self.__dict__

def load_movies_from_csv(file_path: str) -> List[Movie]:
    movies = []
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            movie = Movie(
                movieId=int(row["movieId"]),
                title=row["title"],
                genres=row["genres"]
            )
            movies.append(movie)
    return movies

class Link:
    def __init__(self, movieId: int, imdbId: int, tmdbId: int):
        self.movieId = movieId
        self.imdbId = imdbId
        self.tmdbId = tmdbId

    def to_dict(self):
        return self.__dict__

def load_links_from_csv(file_path: str):
    links = []
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            link = Link(
                movieId=int(row["movieId"]),
                imdbId=int(row["imdbId"]),
                tmdbId=row["tmdbId"]
            )
            links.append(link)
    return links

# Аналогично Rating и Tag
class Rating:
    def __init__(self, userId: int, movieId: int, rating: float, timestamp: int):
        self.userId = userId
        self.movieId = movieId
        self.rating = rating
        self.timestamp = timestamp

    def to_dict(self):
        return self.__dict__

def load_ratings_from_csv(file_path: str):
    ratings = []
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rating = Rating(
                userId=int(row["userId"]),
                movieId=int(row["movieId"]),
                rating=float(row["rating"]),
                timestamp=int(row["timestamp"])
            )
            ratings.append(rating)
    return ratings

class Tag:
    def __init__(self, userId: int, movieId: int, tag: str, timestamp: int):
        self.userId = userId
        self.movieId = movieId
        self.tag = tag
        self.timestamp = timestamp

    def to_dict(self):
        return self.__dict__

def load_tags_from_csv(file_path: str):
    tags = []
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = Tag(
                userId=int(row["userId"]),
                movieId=int(row["movieId"]),
                tag=row["tag"],
                timestamp=int(row["timestamp"])
            )
            tags.append(tag)
    return tags
