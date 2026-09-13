import importlib
import sys


class DummyPool:
    pass


def load_app(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:password@localhost:5432/targeting_db")
    monkeypatch.setenv("AUTH_SERVICE_URL", "http://auth-service")

    import psycopg2.pool

    monkeypatch.setattr(psycopg2.pool, "SimpleConnectionPool", lambda *args, **kwargs: DummyPool())
    sys.modules.pop("app", None)
    module = importlib.import_module("app")
    return module.app


def test_health(monkeypatch):
    client = load_app(monkeypatch).test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_rules_requires_authorization(monkeypatch):
    client = load_app(monkeypatch).test_client()

    response = client.get("/rules/demo-flag")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Authorization header obrigatório"
