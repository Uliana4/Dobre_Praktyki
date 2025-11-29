from fastapi import FastAPI
from app.routers import movies, links, ratings, tags


app = FastAPI(
    title="Movies API",
    version="1.0.0",
    description="Prosty serwis API do pracy z bazą movies.db",
)


# Rejestracja routerów
app.include_router(movies.router)
app.include_router(links.router)
app.include_router(ratings.router)
app.include_router(tags.router)


# Prosty endpoint kontrolny
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Movies API działa. Sprawdź /docs po więcej."
    }


if __name__ == "__main__":
    import uvicorn
    # uruchomienie przez: python -m app.main
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
