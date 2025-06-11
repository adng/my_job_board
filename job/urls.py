from django.urls import path
from .views import JobListCreateView, JobRetrieveUpdateDestroyView

urlpatterns = [
    path("jobs/", JobListCreateView.as_view(), name="job-list-create"),
    path("jobs/<int:pk>/", JobRetrieveUpdateDestroyView.as_view(), name="job-detail"),
]
