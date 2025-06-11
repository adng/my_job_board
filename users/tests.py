import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework_api_key.models import APIKey


@pytest.fixture
def api_key():
    _, key = APIKey.objects.create_key(name="test-key")
    return key


@pytest.fixture
def api_client(api_key):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Api-Key {api_key}")
    return client


@pytest.mark.django_db
def test_signup_creates_user(api_client):
    url = reverse("sign_up")
    email = "testuser@example.com"
    response = api_client.post(url, {"email": email, "password": "pass1234"})
    assert response.status_code == 201
    User = get_user_model()
    assert User.objects.filter(email=email).exists()


@pytest.mark.django_db
def test_signup_duplicate_email(api_client):
    url = reverse("sign_up")
    email = "dupe@example.com"
    password = "pass1234"
    User = get_user_model()
    User.objects.create_user(email=email, password=password)
    response = api_client.post(url, {"email": email, "password": "pass1234"})
    assert response.status_code == 400


@pytest.mark.django_db
def test_signup_invalid_email(api_client):
    url = reverse("sign_up")
    response = api_client.post(
        url, {"email": "not-an-email", "password": "pass"}
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_signup_requires_api_key():
    client = APIClient()
    url = reverse("sign_up")
    response = client.post(
        url, {"email": "noapikey@example.com", "password": "pass"}
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_token_obtain_pair_success(api_client):
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
    url = reverse("token_obtain_pair")
    response = api_client.post(
        url, {"email": "wrong@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_token_refresh(api_client):
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
