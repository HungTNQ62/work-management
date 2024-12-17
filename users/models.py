from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password, phone, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        if not kwargs.get("is_staff") or not kwargs.get("is_superuser"):
            raise ValueError("Superuser must have both is_staff and is_superuser are True")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, default="", unique=True, blank=False, null=False)
    email = models.EmailField(max_length=255, default="", unique=True, blank=True, null=True)
    password = models.CharField(max_length=255, default="", blank=False, null=False)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'user'