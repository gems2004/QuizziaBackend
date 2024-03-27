from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from Bundles.models import Bundle


class User(AbstractUser):
    role = models.CharField(max_length=50)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    bundle_expiry = models.DateField(null=True)
    is_subscribed = models.BooleanField(default=False)
    fk_bundle = models.ForeignKey(Bundle, on_delete=models.PROTECT, default=1)
    subject = models.CharField(max_length=100)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, unique=True)
