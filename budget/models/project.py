from django.db import models

from .subject import Subject


class Project(models.Model):
    book = models.ForeignKey('budget.Book', related_name='projects')
    department = models.ForeignKey(
        'account.Department', on_delete=models.PROTECT, related_name='projects')
    name = models.CharField(max_length=16)

    @property
    def estimated_income(self):
        return sum(subject.estimated_income for subject in self.subjects.filter(kind=Subject.INCOME))

    @property
    def estimated_expense(self):
        return sum(subject.estimated_expense for subject in self.subjects.filter(kind=Subject.EXPENSE))

    @property
    def actual_income(self):
        return sum(subject.actual_income for subject in self.subjects.filter(kind=Subject.INCOME))

    @property
    def actual_expense(self):
        return sum(subject.actual_expense for subject in self.subjects.filter(kind=Subject.EXPENSE))
