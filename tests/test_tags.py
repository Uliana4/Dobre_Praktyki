from fastapi.testclient import TestClient

from app.main import app
from app.database import SessionLocal
from app.models import Tag

client = TestClient(app)


def test_get_tags_list_includes_inserted():
    db = SessionLocal()
    t1 = Tag(userId=1, movieId=10, tag="funny", timestamp=1000)
    t2 = Tag(userId=2, movieId=20, tag="sad", timestamp=2000)
    db.add_all([t1, t2])
    db.commit()
    db.close()

    resp = client.get("/tags")

    assert resp.status_code == 200
    data = resp.json()
    tags = {(t["userId"], t["movieId"], t["tag"]) for t in data}
    assert (1, 10, "funny") in tags
    assert (2, 20, "sad") in tags


def test_get_tag_existing_and_404():
    db = SessionLocal()
    tag_obj = Tag(userId=3, movieId=30, tag="classic", timestamp=3333)
    db.add(tag_obj)
    db.commit()
    db.close()

    ok_resp = client.get("/tags/3/30/classic/3333")
    not_found_resp = client.get("/tags/9/99/nope/999999")

    assert ok_resp.status_code == 200
    body = ok_resp.json()
    assert body["userId"] == 3
    assert body["movieId"] == 30
    assert body["tag"] == "classic"

    assert not_found_resp.status_code == 404


def test_create_tag_adds_row():
    db = SessionLocal()
    count_before = db.query(Tag).count()
    db.close()

    payload = {
        "userId": 4,
        "movieId": 40,
        "tag": "great",
        "timestamp": 4444,
    }

    resp = client.post("/tags/", json=payload)

    assert resp.status_code == 201
    body = resp.json()
    assert body["userId"] == 4
    assert body["movieId"] == 40
    assert body["tag"] == "great"

    db = SessionLocal()
    count_after = db.query(Tag).count()
    created = (
        db.query(Tag)
        .filter(
            Tag.userId == 4,
            Tag.movieId == 40,
            Tag.tag == "great",
            Tag.timestamp == 4444,
        )
        .first()
    )
    db.close()
    assert count_after == count_before + 1
    assert created is not None


def test_update_tag_changes_text():
    db = SessionLocal()
    tag_obj = Tag(userId=5, movieId=50, tag="old", timestamp=5555)
    db.add(tag_obj)
    db.commit()
    db.close()

    payload = {"tag": "new"}
    resp = client.put("/tags/5/50/old/5555", json=payload)

    assert resp.status_code == 200
    body = resp.json()
    assert body["tag"] == "new"

    db = SessionLocal()
    updated = (
        db.query(Tag)
        .filter(
            Tag.userId == 5,
            Tag.movieId == 50,
            Tag.timestamp == 5555,
        )
        .first()
    )
    db.close()
    assert updated.tag == "new"  # type: ignore


def test_delete_tag_removes_row():
    db = SessionLocal()
    tag_obj = Tag(userId=6, movieId=60, tag="temp", timestamp=6666)
    db.add(tag_obj)
    db.commit()
    count_before = db.query(Tag).count()
    db.close()

    delete_resp = client.delete("/tags/6/60/temp/6666")

    assert delete_resp.status_code == 204

    db = SessionLocal()
    exists = (
        db.query(Tag)
        .filter(
            Tag.userId == 6,
            Tag.movieId == 60,
            Tag.tag == "temp",
            Tag.timestamp == 6666,
        )
        .first()
    )
    count_after = db.query(Tag).count()
    db.close()

    assert exists is None
    assert count_after == count_before - 1