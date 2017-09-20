from django.db import models
from budget.models import Subject

class Project(models.Model):
    book = models.ForeignKey('budget.Book', related_name='projects')
    department = models.ForeignKey('account.Department', related_name='projects')
    name = models.CharField(max_length=16)
    kind = models.CharField(max_length=1, choices=KIND_CHOICES)

    @property
    def estimated_income(self):
        total = 0
        subjects = self.subjects.filter(kind=Subject.INCOME)
        for sub in subjects:
            total += sub.estimated_amount
        return total

    @property
    def estimated_expense(self):
        total = 0
        subjects = self.subjects.filter(kind=Subject.EXPENSE)
        for sub in subjects:
            total += sub.estimated_amount
        return total

    @property
    def actual_income(self):
        total = 0
        subjects = self.subjects.filter(kind=Subject.INCOME)
        for sub in subjects:
            total += sub.actual_amount
        return total

    @property
    def actual_expense(self):
        total = 0
        subjects = self.subjects.filter(kind=Subject.EXPENSE)
        for sub in subjects:
            total += sub.actual_amount
        return total
