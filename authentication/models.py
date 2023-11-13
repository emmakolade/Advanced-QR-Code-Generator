from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
  def create_user(self, email, password=None, **extra_fields):
    if not email:
      raise ValueError(_('Email must be provided'))
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save()
    return user
  
  def create_superuser(self, email, password=None, **extra_fields):
     extra_fields.setdefault('is_staff', True)
     extra_fields.setdefault('is_superuser', True)
     return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(_('email address'), unique=True)
  otp = models.IntegerField(_('one time password'), blank=True, null=True)
  is_active = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []
  objects = UserManager()

  def __str__(self):
    return self.email