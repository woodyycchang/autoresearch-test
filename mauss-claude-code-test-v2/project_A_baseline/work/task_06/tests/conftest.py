"""Pytest fixtures for OAuth2 tests."""

import os
import sys

import pytest

# Make project root importable
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from server import create_app  # noqa: E402
from storage import storage  # noqa: E402


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_storage():
    """Wipe in-memory storage between tests so they don't leak state."""
    storage.reset()
    yield
    storage.reset()
