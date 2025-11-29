from fastapi.testclient import TestClient

from app.main import app
from app.database import SessionLocal
from app.models import Rating

client = TestClient(app)


def test_get_ratings_list_includes_inserted():
    db = SessionLocal()
    r1 = Rating(userId=1, movieId=10, rating=4.0, timestamp=1000)
    r2 = Rating(userId=2, movieId=10, rating=3.5, timestamp=2000)
    db.add_all([r1, r2])
    db.commit()
    db.close()

    resp = client.get("/ratings")

    assert resp.status_code == 200
    data = resp.json()
    ratings = {(r["userId"], r["movieId"]) for r in data}
    assert (1, 10) in ratings
    assert (2, 10) in ratings


def test_get_rating_existing_and_404():
    db = SessionLocal()
    rating = Rating(userId=5, movieId=50, rating=5.0, timestamp=5555)
    db.add(rating)
    db.commit()
    db.close()

    ok_resp = client.get("/ratings/5/50/5555")
    not_found_resp = client.get("/ratings/9/9/999999")

    assert ok_resp.status_code == 200
    body = ok_resp.json()
    assert body["userId"] == 5
    assert body["movieId"] == 50
    assert body["timestamp"] == 5555

    assert not_found_resp.status_code == 404


def test_create_rating_adds_row():
    db = SessionLocal()
    count_before = db.query(Rating).count()
    db.close()

    payload = {
        "userId": 7,
        "movieId": 70,
        "rating": 4.5,
        "timestamp": 7777,
    }

    resp = client.post("/ratings/", json=payload)

    assert resp.status_code == 201
    body = resp.json()
    assert body["userId"] == 7
    assert body["movieId"] == 70
    assert body["rating"] == 4.5

    db = SessionLocal()
    count_after = db.query(Rating).count()
    created = (
        db.query(Rating)
        .filter(
            Rating.userId == 7,
            Rating.movieId == 70,
            Rating.timestamp == 7777,
        )
        .first()
    )
    db.close()
    assert count_after == count_before + 1
    assert created is not None


def test_update_rating_changes_value():
    db = SessionLocal()
    rating = Rating(userId=8, movieId=80, rating=2.0, timestamp=8888)
    db.add(rating)
    db.commit()
    db.close()

    payload = {"rating": 4.0}
    resp = client.put("/ratings/8/80/8888", json=payload)

    assert resp.status_code == 200
    body = resp.json()
    assert body["rating"] == 4.0

    db = SessionLocal()
    updated = (
        db.query(Rating)
        .filter(
            Rating.userId == 8,
            Rating.movieId == 80,
            Rating.timestamp == 8888,
        )
        .first()
    )
    db.close()
    assert updated.rating == 4.0  # type: ignore


def test_delete_rating_removes_row():
    db = SessionLocal()
    rating = Rating(userId=9, movieId=90, rating=3.0, timestamp=9999)
    db.add(rating)
    db.commit()
    count_before = db.query(Rating).count()
    db.close()

    delete_resp = client.delete("/ratings/9/90/9999")

    assert delete_resp.status_code == 204

    db = SessionLocal()
    exists = (
        db.query(Rating)
        .filter(
            Rating.userId == 9,
            Rating.movieId == 90,
            Rating.timestamp == 9999,
        )
        .first()
    )
    count_after = db.query(Rating).count()
    db.close()

    assert exists is None
    assert count_after == count_before - 1