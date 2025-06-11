import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_api_key.models import APIKey

from job.models import Job


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
    user = User.objects.create_user(
        email="jobuser@example.com", password="pass1234"
    )
    return user


@pytest.fixture
def obtain_token(user):
    """Obtain JWT access token for the test user."""
    client = APIClient()
    url = reverse("token_obtain_pair")
    response = client.post(
        url, {"email": "jobuser@example.com", "password": "pass1234"}
    )
    assert response.status_code == 200
    return response.data["access"]


@pytest.mark.django_db
def test_job_list(api_client, user):
    """Test job list endpoint."""
    Job.objects.create(
        title="Job1",
        location="Paris",
        description="Desc1",
        contract_type="cdi",
        reference="REF1",
        salary=50000,
        owner=user,
    )
    Job.objects.create(
        title="Job2",
        location="Lyon",
        description="Desc2",
        contract_type="cdd",
        reference="REF2",
        salary=60000,
        owner=user,
    )
    url = reverse("job-list-create")
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_job_create(api_client, user):
    """Test job creation endpoint."""
    api_client.force_authenticate(user=user)
    url = reverse("job-list-create")
    data = {
        "title": "New Job",
        "location": "Remote",
        "description": "Job description",
        "contract_type": "cdi",
        "reference": "REF123",
        "salary": 100000,
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert Job.objects.filter(title="New Job").exists()


@pytest.mark.django_db
def test_job_retrieve(api_client, user):
    """Test job retrieve endpoint."""
    job = Job.objects.create(
        title="Job1",
        location="Paris",
        description="Desc1",
        contract_type="cdi",
        reference="REF1",
        salary=50000,
        owner=user,
    )
    url = reverse("job-detail", args=[job.id])
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["title"] == "Job1"


@pytest.mark.django_db
def test_job_update(api_client, user):
    """Test job update endpoint."""
    job = Job.objects.create(
        title="Job1",
        location="Paris",
        description="Desc1",
        contract_type="cdi",
        reference="REF1",
        salary=50000,
        owner=user,
    )
    api_client.force_authenticate(user=user)
    url = reverse("job-detail", args=[job.id])
    data = {
        "title": "Updated Job",
        "location": "Lyon",
        "description": "Updated Desc",
        "contract_type": "cdd",
        "reference": "REF2",
        "salary": 120000,
    }
    response = api_client.put(url, data)
    assert response.status_code == 200
    job.refresh_from_db()
    assert job.title == "Updated Job"


@pytest.mark.django_db
def test_job_delete(api_client, user):
    """Test job delete endpoint."""
    job = Job.objects.create(
        title="Job1",
        location="Paris",
        description="Desc1",
        contract_type="cdi",
        reference="REF1",
        salary=50000,
        owner=user,
    )
    api_client.force_authenticate(user=user)
    url = reverse("job-detail", args=[job.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    assert not Job.objects.filter(id=job.id).exists()


@pytest.mark.django_db
def test_job_create_with_jwt(user, obtain_token):
    """Test job creation endpoint with JWT access token."""
    client = APIClient()
    token = obtain_token
    url = reverse("job-list-create")
    data = {
        "title": "JWT Job",
        "location": "Remote",
        "description": "Job with JWT",
        "contract_type": "cdi",
        "reference": "JWTREF",
        "salary": 90000,
    }
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = client.post(url, data)
    assert response.status_code == 201
    assert Job.objects.filter(title="JWT Job").exists()


@pytest.mark.django_db
def test_job_update_with_jwt(user, obtain_token):
    """Test job update endpoint with JWT access token."""
    job = Job.objects.create(
        title="JWT Job",
        location="Paris",
        description="Desc1",
        contract_type="cdi",
        reference="JWTREF",
        salary=50000,
        owner=user,
    )
    client = APIClient()
    token = obtain_token
    url = reverse("job-detail", args=[job.id])
    data = {
        "title": "JWT Updated Job",
        "location": "Lyon",
        "description": "Updated Desc JWT",
        "contract_type": "cdd",
        "reference": "JWTREF2",
        "salary": 120000,
    }
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = client.put(url, data)
    assert response.status_code == 200
    job.refresh_from_db()
    assert job.title == "JWT Updated Job"
