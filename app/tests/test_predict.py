"""Tests for ensuring proper predict.py functionality"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_valid_input():
    """Return 200 Success when input is valid."""
    response = client.post(
        '/predict',
        json={
            'symptoms': 'pain'
        }
    )
    body = response.json()
    assert response.status_code == 200
    assert isinstance(item.symptoms, str)


def test_invalid_input():
    """Return 422 Validation Error when symptoms is not a string"""
    response = client.post(
        '/predict',
        json={
            'symptoms': 420
        }
    )
    body = response.json()
    assert response.status_code == 422
    assert 'symptoms' in body['detail'][0]['loc']
    