"""Pytest fixtures for the OAuth2 mock server tests."""

import os
import sys

import pytest

# Ensure the project root is importable so tests can import server/tokens/storage.
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import server  # noqa: E402
import storage  # noqa: E402


@pytest.fixture
def store():
    """Fresh in-memory storage per test."""
    s = storage.Storage()
    return s


@pytest.fixture
def app(store):
    application = server.create_app(storage=store)
    application.config.update(TESTING=True)
    return application


@pytest.fixture
def client(app):
    return app.test_client()
