"""Tests for app.py module."""
import pytest

from app import app


@pytest.fixture(name="client")
def setup_fixture():
    """Test app setup."""
    app.config['TESTING'] = True
    with app.test_client() as _client:
        yield _client


def test_homepage(client):
    """basic test to make sure ™ sign is present on the homepage."""
    response = client.get('/')
    assert response.status_code == 200
    assert '™' in response.text


def test_custom_page(client):
    """Test to make sure punctuation marks are accounted for."""
    response = client.get('/item?id=13713480')
    assert response.status_code == 200
    assert 'header™,' in response.text


def test_feedback_page(client):
    """Test the url from the feedback email."""
    response = client.get('/item?id=16090815')
    assert response.status_code == 200

    # make sure it's not nitens™.org
    assert "http://nitens.org/taraborelli/TeXOpenType" in response.text
    assert "&thinsp;" in response.text
    assert "mostly™" in response.text
