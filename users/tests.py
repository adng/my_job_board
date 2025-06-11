import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_api_key.models import APIKey


@pytest.fixture
def api_key():
    # Create API key for test client
    _, key = APIKey.objects.create_key(name="test-key")
    return key


@pytest.fixture
def api_client(api_key):
    # API client with API key
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    return client


@pytest.fixture
def user(db):
    # Create a test user
    User = get_user_model()
    return User.objects.create_user(
        email="testuser2@example.com", password="pass1234"
    )


@pytest.mark.django_db
def test_signup_creates_user(api_client):
    """Test user registration."""
    url = reverse("sign_up")
    email = "testuser@example.com"
    response = api_client.post(url, {"email": email, "password": "pass1234"})
    assert response.status_code == 201
    User = get_user_model()
    assert User.objects.filter(email=email).exists()


@pytest.mark.django_db
def test_signup_duplicate_email(api_client):
    """Test duplicate email registration."""
    url = reverse("sign_up")
    email = "dupe@example.com"
    password = "pass1234"
    User = get_user_model()
    User.objects.create_user(email=email, password=password)
    response = api_client.post(url, {"email": email, "password": "pass1234"})
    assert response.status_code == 400


@pytest.mark.django_db
def test_signup_invalid_email(api_client):
    """Test invalid email registration."""
    url = reverse("sign_up")
    response = api_client.post(
        url, {"email": "not-an-email", "password": "pass"}
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_signup_requires_api_key():
    """Test registration without API key."""
    client = APIClient()
    url = reverse("sign_up")
    response = client.post(
        url, {"email": "noapikey@example.com", "password": "pass"}
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_token_obtain_pair_success(api_client):
    """Test JWT token obtain with valid credentials."""
    User = get_user_model()
    email = "jwtuser@example.com"
    password = "jwtpass123"
    User.objects.create_user(email=email, password=password)
    url = reverse("token_obtain_pair")
    response = api_client.post(url, {"email": email, "password": password})
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_token_obtain_pair_invalid_credentials(api_client):
    """Test JWT token obtain with invalid credentials."""
    url = reverse("token_obtain_pair")
    response = api_client.post(
        url, {"email": "wrong@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_token_refresh(api_client):
    """Test JWT token refresh."""
    User = get_user_model()
    email = "refreshuser@example.com"
    password = "refreshpass123"
    User.objects.create_user(email=email, password=password)
    obtain_url = reverse("token_obtain_pair")
    obtain_response = api_client.post(
        obtain_url, {"email": email, "password": password}
    )
    refresh_token = obtain_response.data["refresh"]
    refresh_url = reverse("token_refresh")
    refresh_response = api_client.post(refresh_url, {"refresh": refresh_token})
    assert refresh_response.status_code == 200
    assert "access" in refresh_response.data


@pytest.mark.django_db
def test_signout_success(api_client):
    """Test sign out (refresh token blacklist)."""
    User = get_user_model()
    email = "logoutuser@example.com"
    password = "logoutpass123"
    User.objects.create_user(email=email, password=password)
    # Obtain tokens
    obtain_url = reverse("token_obtain_pair")
    obtain_response = api_client.post(
        obtain_url, {"email": email, "password": password}
    )
    refresh_token = obtain_response.data["refresh"]
    # Sign out
    signout_url = reverse("sign_out")
    api_client.force_authenticate(user=User.objects.get(email=email))
    response = api_client.post(signout_url, {"refresh": refresh_token})
    assert response.status_code == 205
    assert response.data["detail"] == "Signed out."


@pytest.mark.django_db
def test_signout_invalid_token(api_client, user):
    """Test sign out with invalid refresh token."""
    api_client.force_authenticate(user=user)
    signout_url = reverse("sign_out")
    response = api_client.post(signout_url, {"refresh": "invalidtoken"})
    assert response.status_code == 400
    assert "detail" in response.data
