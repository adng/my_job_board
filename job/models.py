from django.db import models
from django.conf import settings


class Job(models.Model):
    """
    Job posting model.
    """

    # Contract type choices
    ALTERNANCE = "alternance"
    CDD = "cdd"
    CDI = "cdi"
    FREELANCE = "freelance"
    INTERIM = "interim"

    CONTRACT_TYPE = (
        (ALTERNANCE, "Alternance"),
        (CDD, "CDD"),
        (CDI, "CDI"),
        (FREELANCE, "Freelance"),
        (INTERIM, "Intérim"),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobs",  # User who posted the job
    )
    reference = models.CharField(blank=True)  # Optional job reference
    title = models.CharField()  # Job title
    location = models.CharField()  # Job location
    description = models.TextField()  # Job description
    creation_date = models.DateField(auto_now_add=True)  # Date created
    salary = models.IntegerField(null=True, blank=True)  # Optional salary
    contract_type = models.CharField(choices=CONTRACT_TYPE)  # Contract type
