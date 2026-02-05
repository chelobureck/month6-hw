from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager

class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    phone_num = models.CharField(max_length=13, null=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    birthday = models.DateField(null=True)
    last_login = models.DateTimeField(null=True, blank=True)
    registration_source = models.CharField(max_length=50, default='local')

    objects = CustomUserManager()

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['phone_num']

    def __str__(self) -> str:
        return self.username

