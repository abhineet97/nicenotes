from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError("The given mobile must be set")
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, mobile, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(mobile, password, **extra_fields)

    def create_superuser(self, mobile, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(mobile, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    full_name = models.CharField(max_length=40)
    mobile = models.CharField(max_length=10, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "mobile"
    EMAIL_FIELD = "mobile"
    REQUIRED_FIELD = ["full_name"]

    objects = CustomUserManager()

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name
