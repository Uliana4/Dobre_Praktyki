import csv
import os
from typing import Callable, List
from database import Movie, Link, Rating, Tag, User, SessionLocal
import bcrypt

def load_csv_to_db(filename: str, model_class, row_mapper: Callable):
    session = SessionLocal()
    path = os.path.join(os.path.dirname(__file__), "database", filename)
    objects = []
    
    with open(path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            obj = row_mapper(row)
            objects.append(obj)
    
    session.bulk_save_objects(objects)
    session.commit()
    session.close()

def load_movies():
    def map_movie(row):
        return Movie(
            movieId=int(row["movieId"]), 
            title=row["title"], 
            genres=row["genres"]
        )
    load_csv_to_db("movies.csv", Movie, map_movie)

def load_links():
    def map_link(row):
        return Link(
            movieId=int(row["movieId"]), 
            imdbId=row["imdbId"], 
            tmdbId=row["tmdbId"]
        )
    load_csv_to_db("links.csv", Link, map_link)

def load_ratings():
    def map_rating(row):
        return Rating(
            userId=int(row["userId"]), 
            movieId=int(row["movieId"]), 
            rating=float(row["rating"]), 
            timestamp=int(row["timestamp"])
        )
    load_csv_to_db("ratings.csv", Rating, map_rating)

def load_tags():
    def map_tag(row):
        return Tag(
            userId=int(row["userId"]), 
            movieId=int(row["movieId"]), 
            tag=row["tag"], 
            timestamp=int(row["timestamp"])
        )
    load_csv_to_db("tags.csv", Tag, map_tag)

def create_admin_user():
    """Create default admin user if not exists"""
    session = SessionLocal()
    
    # Check if admin already exists
    existing_admin = session.query(User).filter(User.username == "admin").first()
    if existing_admin:
        print("Admin user already exists, skipping...")
        session.close()
        return
    
    # Create admin user
    password_hash = bcrypt.hashpw(b"admin123", bcrypt.gensalt())
    admin = User(
        username="admin",
        password_hash=password_hash.decode('utf-8'),
        roles=["ROLE_USER", "ROLE_ADMIN"]
    )
    session.add(admin)
    session.commit()
    session.close()
    print("Admin user created (username: admin, password: admin123)")

def main():
    print("Loading movies...")
    load_movies()
    print("Loading links...")
    load_links()
    print("Loading ratings...")
    load_ratings()
    print("Loading tags...")
    load_tags()
    print("Creating admin user...")
    create_admin_user()
    print("Done!")

if __name__ == "__main__":
    main()