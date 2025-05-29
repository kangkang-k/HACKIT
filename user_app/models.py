from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    completed_tasks = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    code_age = models.IntegerField(default=0)


class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
