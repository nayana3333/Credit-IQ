import os
import tempfile

from app import create_app


def test_unexpected_exception_returns_clean_json_not_a_traceback():
    """PROPAGATE_EXCEPTIONS=False mimics production (gunicorn, no debug mode),
    where the errorhandler in logging_config.py is actually the one that
    handles an unhandled exception, instead of pytest re-raising it."""
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)
    app = create_app({
        "TESTING": True,
        "PROPAGATE_EXCEPTIONS": False,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "JWT_SECRET_KEY": "test-secret-key",
        "SECRET_KEY": "test-secret-key",
        "RATELIMIT_ENABLED": False,
    })

    @app.get("/__boom")
    def boom():
        raise RuntimeError("simulated failure")

    try:
        client = app.test_client()
        res = client.get("/__boom")
        assert res.status_code == 500
        assert res.get_json() == {"error": "An unexpected error occurred. Please try again."}
    finally:
        os.unlink(db_path)


def test_404_is_not_swallowed_by_the_generic_error_handler(client):
    res = client.get("/api/v1/this-route-does-not-exist")
    assert res.status_code == 404
