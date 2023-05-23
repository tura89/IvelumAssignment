import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert '™' in response.text


def test_custom_page(client):
    response = client.get('/item?id=13713480')
    assert response.status_code == 200
    assert 'header™,' in response.text

