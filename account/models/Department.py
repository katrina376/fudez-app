from django.db import models
from account.models import User

class DepartmentManager(models.Manager):
    def add(self, name, id):
        if (id is None):
            raise ValueError("Department ID is not specified: {}".format(name))
        elif (len(self.filter(id=id)) > 0):
            exist = self.get(id=id)
            raise ValueError("Department ID already exists: Unique ID {0}, Exist Name {1}".format(exist.id, exist.name))
        else:
            department = self.create(
                name=name,
                id=id
            )
            return department

class Department(models.Model):
    name = models.CharField(max_length=16)
    fa = models.ForeignKey(User, null=True)

    objects = DepartmentManager()

    def set_fa(self, fa):
        self.fa = fa
        self.save()
