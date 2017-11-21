import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

from account.models import Department

class User(AbstractBaseUser, PermissionsMixin):
    # Kind Choices
    DEPARTMENT = 'D'
    STAFF = 'S'
    CHIEF = 'C'
    PRESIDENT = 'P'
    AUDIT = 'A'
    ENGINEER = 'E'
    KIND_CHOICES = (
        (DEPARTMENT, '一般單位請款帳號'),
        (STAFF, '財務部部員'),
        (CHIEF, '財務部部長'),
        (PRESIDENT, '會長、議長、院務會議'),
        (AUDIT, '審查'),
        (ENGINEER, '工程師')
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=16, primary_key=True, unique=True)
    name = models.CharField(max_length=16)
    email = models.EmailField()

    department = models.ForeignKey('account.Department', on_delete=models.PROTECT, related_name='users')
    kind = models.CharField(max_length=1, choices=KIND_CHOICES, default=DEPARTMENT)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email', 'kind', 'department']

    def get_long_name(self):
        return self.name

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.username
