from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.db import models


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=100, null=True, blank=True, unique=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    role = models.CharField(max_length=20, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ['email']
    objects = UserManager()

    def __str__(self):
        return self.email

    # def save(self, *args, **kwargs):
    #     if self.password:
    #         self.password = self.set_password(self.password)
    #         return super().save(*args, **kwargs)


class Content(models.Model):
    author = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=30, null=True, blank=True)
    body = models.CharField(max_length=300, null=True, blank=True)
    summary = models.CharField(max_length=61, null=True, blank=True)
    file_name = models.FileField(upload_to="media/", max_length=254, null=True, blank=True)

