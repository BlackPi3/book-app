from fastapi.testclient import TestClient

from backend.app.main import app, InMemoryRepo, get_repo


def make_client() -> TestClient:
    # Fresh repo per test
    repo = InMemoryRepo()
    app.dependency_overrides[get_repo] = lambda: repo
    return TestClient(app)


def test_health_ok():
    client = make_client()
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_get_books_empty():
    client = make_client()
    resp = client.get("/books")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_post_books_creates_and_returns_book():
    client = make_client()
    payload = {"title": "Clean Code", "author": "Robert C. Martin", "created_by": "alice"}
    resp = client.post("/books", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == payload["title"]
    assert data["author"] == payload["author"]
    assert data["created_by"] == payload["created_by"]
    assert "id" in data and data["id"]
    assert "created_at" in data and data["created_at"]
    assert resp.headers["Location"].startswith("/books/")
    # Appears in list
    list_resp = client.get("/books")
    assert list_resp.status_code == 200
    ids = [item["id"] for item in list_resp.json()["items"]]
    assert data["id"] in ids


def test_filter_created_from_inclusive():
    client = make_client()
    r1 = client.post("/books", json={"title": "B1", "author": "A1", "created_by": "u"})
    assert r1.status_code == 201
    ts = r1.json()["created_at"]
    rlist = client.get(f"/books?created_from={ts}")
    assert rlist.status_code == 200
    ids = [item["id"] for item in rlist.json()["items"]]
    assert r1.json()["id"] in ids
