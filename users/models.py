from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy
from .managers import UserManager
import uuid

# Create your models here.
class User(models.Model):
    objects = UserManager()