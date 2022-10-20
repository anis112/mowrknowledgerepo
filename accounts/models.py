from django.contrib.auth.models import AbstractUser
from django.db import models

from knowledgebase.models import Organization


# Create your models here.
class CustomUser(AbstractUser):
    is_organization_admin = models.BooleanField(default=False)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True)
