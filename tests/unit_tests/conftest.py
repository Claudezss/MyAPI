import pytest

from flask_app.wsgi import app


@pytest.fixture(scope="module")
def client():
    app.config["TESTING"] = True

    client = app.test_client()
    return client
