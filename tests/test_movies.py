from fastapi.testclient import TestClient

from app.main import app
from app.database import SessionLocal
from app.models import Movie

client = TestClient(app)


def test_get_movies_list_returns_our_inserted_movies():
    # arrange – dodajemy 2 filmy do bazy
    db = SessionLocal()
    m1 = Movie(title="Test Movie A", genres="Action")
    m2 = Movie(title="Test Movie B", genres="Comedy")
    db.add_all([m1, m2])
    db.commit()
    db.close()

    # act
    response = client.get("/movies")

    # assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # sprawdzamy, że NASZE filmy są na liście
    titles = {m["title"] for m in data}
    assert "Test Movie A" in titles
    assert "Test Movie B" in titles


def test_get_movie_existing_and_404():
    db = SessionLocal()
    # arrange – film istniejący
    movie = Movie(title="Existing Movie", genres="Drama")
    db.add(movie)
    db.commit()
    movie_id = movie.movieId
    db.close()

    # act – istniejący
    ok_response = client.get(f"/movies/{movie_id}")
    # act – nieistniejący
    not_found_response = client.get("/movies/999999999")

    # assert – istniejący
    assert ok_response.status_code == 200
    body = ok_response.json()
    assert body["movieId"] == movie_id
    assert body["title"] == "Existing Movie"

    # assert – nieistniejący
    assert not_found_response.status_code == 404


def test_create_movie_adds_new_row():
    db = SessionLocal()
    count_before = db.query(Movie).count()
    db.close()

    payload = {
        "title": "New Movie From Test",
        "genres": "Sci-Fi|Action",
    }

    # act
    response = client.post("/movies/", json=payload)

    # assert odpowiedzi
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "New Movie From Test"
    assert body["genres"] == "Sci-Fi|Action"
    assert "movieId" in body

    # assert w bazie
    db = SessionLocal()
    count_after = db.query(Movie).count()
    db.close()
    assert count_after == count_before + 1


def test_update_movie_changes_data():
    # arrange – tworzymy film
    db = SessionLocal()
    movie = Movie(title="Old title", genres="Old genre")
    db.add(movie)
    db.commit()
    movie_id = movie.movieId
    db.close()

    payload = {
        "title": "New title",
        "genres": "New genre",
    }

    # act
    response = client.put(f"/movies/{movie_id}", json=payload)

    # assert odpowiedzi
    assert response.status_code == 200
    body = response.json()
    assert body["movieId"] == movie_id
    assert body["title"] == "New title"
    assert body["genres"] == "New genre"

    # assert w bazie
    db = SessionLocal()
    updated = db.query(Movie).filter(Movie.movieId == movie_id).first()
    db.close()
    assert updated.title == "New title" # type: ignore
    assert updated.genres == "New genre" # type: ignore


def test_delete_movie_removes_row():
    # arrange – film do usunięcia
    db = SessionLocal()
    movie = Movie(title="To delete", genres="Action")
    db.add(movie)
    db.commit()
    movie_id = movie.movieId
    count_before = db.query(Movie).count()
    db.close()

    # act
    delete_response = client.delete(f"/movies/{movie_id}")

    # assert status
    assert delete_response.status_code == 204

    # assert w bazie
    db = SessionLocal()
    exists = db.query(Movie).filter(Movie.movieId == movie_id).first()
    count_after = db.query(Movie).count()
    db.close()
    assert exists is None
    assert count_after == count_before - 1