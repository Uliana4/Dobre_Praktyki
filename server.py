from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from database import Movie, Link, Rating, Tag, User, SessionLocal
import bcrypt
import jwt
import os

app = FastAPI()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1

# Dependency injection for db session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT verification dependency
def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    try:
        # Expected format: "Bearer <token>"
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Admin role verification dependency
def verify_admin(current_user: dict = Depends(verify_token)):
    if "ROLE_ADMIN" not in current_user.get("roles", []):
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

# Pydantic schemas for response models
class MovieSchema(BaseModel):
    movieId: int
    title: str
    genres: str

    class Config:
        from_attributes = True

class LinkSchema(BaseModel):
    movieId: int
    imdbId: str
    tmdbId: str

    class Config:
        from_attributes = True

class RatingSchema(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int

    class Config:
        from_attributes = True

class TagSchema(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int

    class Config:
        from_attributes = True

# Create schemas (without id for POST requests)
class MovieCreate(BaseModel):
    movieId: int
    title: str
    genres: str

class LinkCreate(BaseModel):
    movieId: int
    imdbId: str
    tmdbId: str

class RatingCreate(BaseModel):
    userId: int
    movieId: int
    rating: float
    timestamp: int

class TagCreate(BaseModel):
    userId: int
    movieId: int
    tag: str
    timestamp: int

class UserSchema(BaseModel):
    id: int
    username: str
    roles: List[str]

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str
    roles: Optional[List[str]] = ["ROLE_USER"]

class LoginData(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@app.get("/")
def read_root():
    return {"hello": "world"}

# ==================== MOVIES CRUD ====================

@app.get("/movies", response_model=List[MovieSchema])
def get_movies(db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    movies = db.query(Movie).all()
    return movies

@app.get("/movies/{movie_id}", response_model=MovieSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.post("/movies", response_model=MovieSchema, status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    db_movie = Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.put("/movies/{movie_id}", response_model=MovieSchema)
def update_movie(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    db_movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    for key, value in movie.model_dump().items():
        setattr(db_movie, key, value)
    
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.delete("/movies/{movie_id}", status_code=status.HTTP_200_OK)
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    db_movie = db.query(Movie).filter(Movie.movieId == movie_id).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    db.delete(db_movie)
    db.commit()
    return {"message": "Movie deleted successfully"}

# ==================== LINKS CRUD ====================

@app.get("/links", response_model=List[LinkSchema])
def get_links(db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    links = db.query(Link).all()
    return links

@app.get("/links/{link_id}", response_model=LinkSchema)
def get_link(link_id: int, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    link = db.query(Link).filter(Link.movieId == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link

@app.post("/links", response_model=LinkSchema, status_code=status.HTTP_201_CREATED)
def create_link(link: LinkCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    db_link = Link(**link.model_dump())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

@app.put("/links/{link_id}", response_model=LinkSchema)
def update_link(link_id: int, link: LinkCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    db_link = db.query(Link).filter(Link.movieId == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    for key, value in link.model_dump().items():
        setattr(db_link, key, value)
    
    db.commit()
    db.refresh(db_link)
    return db_link

@app.delete("/links/{link_id}", status_code=status.HTTP_200_OK)
def delete_link(link_id: int, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    db_link = db.query(Link).filter(Link.movieId == link_id).first()
    if not db_link:
        raise HTTPException(status_code=404, detail="Link not found")
    
    db.delete(db_link)
    db.commit()
    return {"message": "Link deleted successfully"}

# ==================== RATINGS CRUD ====================

@app.get("/ratings", response_model=List[RatingSchema])
def get_ratings(db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    ratings = db.query(Rating).all()
    return ratings

@app.get("/ratings/{rating_id}", response_model=RatingSchema)
def get_rating(rating_id: int, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating

@app.post("/ratings", response_model=RatingSchema, status_code=status.HTTP_201_CREATED)
def create_rating(rating: RatingCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    db_rating = Rating(**rating.model_dump())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@app.put("/ratings/{rating_id}", response_model=RatingSchema)
def update_rating(rating_id: int, rating: RatingCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    for key, value in rating.model_dump().items():
        setattr(db_rating, key, value)
    
    db.commit()
    db.refresh(db_rating)
    return db_rating

@app.delete("/ratings/{rating_id}", status_code=status.HTTP_200_OK)
def delete_rating(rating_id: int, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    db.delete(db_rating)
    db.commit()
    return {"message": "Rating deleted successfully"}

# ==================== TAGS CRUD ====================

@app.get("/tags", response_model=List[TagSchema])
def get_tags(db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    tags = db.query(Tag).all()
    return tags

@app.get("/tags/{tag_id}", response_model=TagSchema)
def get_tag(tag_id: int, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@app.post("/tags", response_model=TagSchema, status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    db_tag = Tag(**tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@app.put("/tags/{tag_id}", response_model=TagSchema)
def update_tag(tag_id: int, tag: TagCreate, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    for key, value in tag.model_dump().items():
        setattr(db_tag, key, value)
    
    db.commit()
    db.refresh(db_tag)
    return db_tag

@app.delete("/tags/{tag_id}", status_code=status.HTTP_200_OK)
def delete_tag(tag_id: int, db: Session = Depends(get_db), current_user: dict = Depends(verify_token)):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(db_tag)
    db.commit()
    return {"message": "Tag deleted successfully"}

# ==================== USERS CRUD ====================

@app.post("/users", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    # Check if trying to create admin user
    if "ROLE_ADMIN" in user.roles:
        # Admin role requires authentication and ROLE_ADMIN permission
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization required to create admin user")
        
        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid authorization header format")
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if "ROLE_ADMIN" not in payload.get("roles", []):
                raise HTTPException(status_code=403, detail="Admin access required to create admin user")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Hash password
    password_hash = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    
    # Create new user
    db_user = User(
        username=user.username,
        password_hash=password_hash.decode('utf-8'),
        roles=user.roles
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ==================== AUTH ====================

@app.post("/login", response_model=TokenResponse)
def login(data: LoginData, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Verify password
    if not bcrypt.checkpw(data.password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Generate JWT token
    payload = {
        "sub": user.username,
        "user_id": user.id,
        "roles": user.roles,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return {"access_token": token, "token_type": "bearer"}

@app.get("/user_details")
def get_user_details(current_user: dict = Depends(verify_token)):
    return {
        "username": current_user.get("sub"),
        "user_id": current_user.get("user_id"),
        "roles": current_user.get("roles"),
        "token_issued_at": current_user.get("iat"),
        "token_expires_at": current_user.get("exp")
    }