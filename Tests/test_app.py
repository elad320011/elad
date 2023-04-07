import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_login(client):
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code == 302  # redirect to home page
    assert response.headers['Location'] == 'http://localhost/home'

def test_register(client):
    response = client.post('/register', data={'email': 'test@example.com', 'password': 'password'})
    assert response.status_code == 302  # redirect to login page
    assert response.headers['Location'] == 'http://localhost/login'

def test_home(client):
    response = client.get('/home')
    assert response.status_code == 200  # successful request
    assert b'Welcome to the home page!' in response.data

def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200  # successful request
    assert b'This is the about page.' in response.data
