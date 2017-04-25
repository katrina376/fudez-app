from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, password, kind, department):
        user = self.model(
            username=username,
            kind=kind,
            department=department
        )
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email', 'department', 'kind']

    # Kind Choices
    D_STAFF = 'S'
    D_CHIEF = 'C'
    F_STAFF = 'A'
    F_CHEIF = 'F'
    PRESIDENT = 'P'
    KIND_CHOICES = (
        (D_STAFF, '請款部員'),
        (D_CHIEF, '部長'),
        (F_STAFF, '財務部部員'),
        (F_CHEIF, '財務部部長'),
        (PRESIDENT, '會長')
    )

    username = models.CharField(max_length=16, primary_key=True)
    name = models.CharField(max_length=16)
    email = models.EmailField()

    department = models.ForeignKey('account.Department')
    kind = models.CharField(max_length=1, choices=KIND_CHOICES)

    create_time = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    def __str__(self):
        return self.username
