from django.db import models

class Book(models.Model):
    department = models.ForeignKey('account.Department')
    session = models.ForeignKey('budget.Session')

    title = models.CharField(max_length=32)
    description = models.TextField()

    is_active = models.BooleanField(default=True)
