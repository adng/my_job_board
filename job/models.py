from django.db import models


class Job(models.Model):
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

    reference = models.CharField(blank=True)
    title = models.CharField()
    location = models.CharField()
    description = models.TextField()
    creation_date = models.DateField(auto_now_add=True)
    salary = models.IntegerField(null=True, blank=True)
    contract_type = models.CharField(choices=CONTRACT_TYPE)
