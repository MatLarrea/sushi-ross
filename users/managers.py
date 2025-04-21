from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    """Override of BaseUserManager for our Custom User in system"""

    use_in_migrations = True

    def _create_user(self, name, lastname, email, password, **extra_fields):
        """help method for create a user"""
        if not name or not lastname or not email:
            raise ValueError("The given data must be set")
        email = self.normalize_email(email)
        user = self.model(name=name, lastname=lastname, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, lastname, email, password, **extra_fields):
        """
        Create a normal user, with minimum required args:
        name, lastname, email, password
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, lastname, email, password, **extra_fields)

    def create_superuser(self, name, lastname, email, password, **extra_fields):
        """
        Create a super user (root), with minimum required args:
        name, lastname, email, password
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(name, lastname, email, password, **extra_fields)