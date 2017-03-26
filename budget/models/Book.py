from django.db import models

class Book(models.Model):
    department = models.ForeignKey('account.models.Department')
    session = model.ForeignKey('budget.models.Session')

    title = models.CharField(max_length=32)
    description = models.TextField()

    is_active = models.BooleanField(default=True)
