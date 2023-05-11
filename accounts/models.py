from django.contrib.auth.models import AbstractUser
from django.db import models

from knowledgebase.models import Organization


# Create your models here.
class CustomUser(AbstractUser):
    is_organization_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
     
    # def encoded_id(self):
    #     import base64
    #     return base64.b64encode(str(self.id))

    # def decode_id(self, id):
    #     import base64
    #     return base64.b64decode(id)
