import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy

from .managers import UserManager

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """Data model for custom user in system"""

    name = models.CharField(
        gettext_lazy("first name"), max_length=30, blank=False, null=False
    )
    lastname = models.CharField(
        gettext_lazy("last name"), max_length=30, blank=False, null=False
    )
    cellphone = models.CharField(
        gettext_lazy("cellphone"), max_length=10, blank=False, null=False
    )
    email = models.EmailField(gettext_lazy("email address"), unique=True)
    country = models.CharField(
        gettext_lazy("country"),
        max_length=128,
        null=False,
        blank=False,
        default="Chile",
    )
    date_joined = models.DateTimeField(gettext_lazy("date joined"), auto_now_add=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    is_staff = models.BooleanField(
        gettext_lazy("staff status"),
        default=False,
        help_text=gettext_lazy(
            "Designates wheter the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(gettext_lazy("active"), default=True)
    objects = UserManager()
    role = models.CharField(max_length=20,
                                 choices=[
                                            ('DELIVERY', 'delivery'),
                                            ('ADMINISTRADOR', 'administrador'),
                                            ('CLIENTE', 'cliente'),
                                            ('CAJERO', 'cajero'),
                                        ])
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","cellphone"]

    class Meta:
        """Meta definitions for model"""

        verbose_name = gettext_lazy("user")
        verbose_name_plural = gettext_lazy("users")

    @property
    def full_name(self):
        """
        Returns the full name.
        """
        full_name = f"{self.name} {self.lastname}"
        return full_name.strip()

    def get_short_name(self):
        """
        Returns a short name for the user.
        """
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this user.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.full_name