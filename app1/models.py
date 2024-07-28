from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name=models.CharField(max_length=255, blank=True ,null=True)
    
    class meta:
        verbose_name='User'
        verbose_name_plural='Users'
