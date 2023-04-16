import os
import pytest
from app import app

# Initialize test client with application context
@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

# Test home page
def test_home(client):
    response = client.get('/')
    assert response.status_code == 302
    assert response.headers['Location'] == 'http://localhost:30007/login'

# Test login with correct credentials
def test_login(client):
    response = client.post('/login', data=dict(email=os.getenv("TEST_EMAIL"), password=os.getenv("TEST_PASSWORD")), follow_redirects=True)
    assert response.status_code == 200
    assert b'Home Page' in response.data

# Test login with incorrect credentials
def test_login_invalid(client):
    response = client.post('/login', data=dict(email='invalid@example.com', password='invalid'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email or password.' in response.data

# Test registration with correct input
def test_register(client):
    response = client.post('/register', data=dict(email='test@example.com', password='test'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Please check your email to verify your account.' in response.data

# Test registration with existing email
def test_register_existing(client):
    response = client.post('/register', data=dict(email=os.getenv("TEST_EMAIL"), password=os.getenv("TEST_PASSWORD")), follow_redirects=True)
    assert response.status_code == 200
    assert b'A user with this email address already exists.' in response.data

# Test email verification with correct input
def test_verify(client):
    response = client.get('/verify?email=' + os.getenv("TEST_EMAIL") + '&code=' + os.getenv("TEST_CODE"), follow_redirects=True)
    assert response.status_code == 200
    assert b'Your account has been successfully verified!' in response.data

# Test email verification with incorrect email
def test_verify_invalid_email(client):
    response = client.get('/verify?email=invalid@example.com&code=' + os.getenv("TEST_CODE"), follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid verification link.' in response.data

# Test email verification with incorrect code
def test_verify_invalid_code(client):
    response = client.get('/verify?email=' + os.getenv("TEST_EMAIL") + '&code=invalid', follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid verification code.' in response.data
