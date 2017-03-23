from django.contrib.auth.models import AbstractBaseUser, AbstractBaseUserManager
from django.db import models

class UserManager(AbstractBaseUserManager):
    def new(self, username, password, identity, department):
        user = self.model(
            username=username,
            identity=identity,
            department=department
        )
        # TODO: What if department_id cannot match department?
        user.set_password(password)
        user.save()
        return user

class User(AbstractBaseUser):
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['identity', 'department']

    # Identity Choices
    D_STAFF = 'S'
    D_CHIEF = 'C'
    F_STAFF = 'A'
    F_CHEIF = 'F'
    IDENTITY_CHOICES = (
        (D_STAFF, '請款部員'),
        (D_CHIEF, '部長'),
        (F_STAFF, '財務部部員'),
        (F_CHEIF, '財務部部長'),
    )

    username = models.CharField(max_length=16, unique=True)

    department = models.ForeignKey('account.models.Department')
    identity = models.CharField(max_length=1, choices=IDENTITY_CHOICES)

    create_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    def activate(self):
        self.is_active = True
        self.save()
        return self

    def deactivate(self):
        self.is_active = False
        self.save()
        return self

    def set_department(self, department):
        self.department = department
        return self

    def __str__(self):
        return self.username
