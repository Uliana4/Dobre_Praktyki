from sqlalchemy.orm import sessionmaker
from app.models import get_engine


# Tworzymy silnik bazy danych (SQLite w Twoim przypadku)
engine = get_engine("movies.db")

# Klasa zarządzająca sesjami z bazą
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Dependency dla FastAPI — tworzy i zamyka sesję
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()