from fastapi.testclient import TestClient

from app.main import app
from app.database import SessionLocal
from app.models import Link

client = TestClient(app)


def test_get_links_list_includes_inserted():
    db = SessionLocal()
    l1 = Link(movieId=1001, imdbId=111111, tmdbId=222222)
    l2 = Link(movieId=1002, imdbId=333333, tmdbId=444444)
    db.add_all([l1, l2])
    db.commit()
    db.close()

    response = client.get("/links")

    assert response.status_code == 200
    data = response.json()
    movie_ids = {l["movieId"] for l in data}
    assert 1001 in movie_ids
    assert 1002 in movie_ids


def test_get_link_existing_and_404():
    db = SessionLocal()
    link = Link(movieId=2001, imdbId=123, tmdbId=456)
    db.add(link)
    db.commit()
    db.close()

    ok_resp = client.get("/links/2001")
    not_found_resp = client.get("/links/999999")

    assert ok_resp.status_code == 200
    assert ok_resp.json()["movieId"] == 2001

    assert not_found_resp.status_code == 404


def test_create_link_adds_row():
    db = SessionLocal()
    count_before = db.query(Link).count()
    db.close()

    payload = {"movieId": 3001, "imdbId": 999999, "tmdbId": 888888}

    response = client.post("/links/", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["movieId"] == 3001
    assert body["imdbId"] == 999999
    assert body["tmdbId"] == 888888

    db = SessionLocal()
    count_after = db.query(Link).count()
    created = db.query(Link).filter(Link.movieId == 3001).first()
    db.close()
    assert count_after == count_before + 1
    assert created is not None


def test_update_link_changes_data():
    db = SessionLocal()
    link = Link(movieId=4001, imdbId=1, tmdbId=2)
    db.add(link)
    db.commit()
    db.close()

    payload = {"imdbId": 10, "tmdbId": 20}
    response = client.put("/links/4001", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["imdbId"] == 10
    assert body["tmdbId"] == 20

    db = SessionLocal()
    updated = db.query(Link).filter(Link.movieId == 4001).first()
    db.close()
    assert updated.imdbId == 10 # type: ignore
    assert updated.tmdbId == 20 # type: ignore


def test_delete_link_removes_row():
    db = SessionLocal()
    link = Link(movieId=5001, imdbId=111, tmdbId=222)
    db.add(link)
    db.commit()
    count_before = db.query(Link).count()
    db.close()

    delete_resp = client.delete("/links/5001")

    assert delete_resp.status_code == 204

    db = SessionLocal()
    exists = db.query(Link).filter(Link.movieId == 5001).first()
    count_after = db.query(Link).count()
    db.close()
    assert exists is None
    assert count_after == count_before - 1