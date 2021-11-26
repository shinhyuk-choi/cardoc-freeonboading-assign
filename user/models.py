from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'user'

    num_id = models.BigAutoField(primary_key=True)
    id = models.CharField(
        unique=True,
        max_length=20
    )
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'id'
    objects = UserManager()



