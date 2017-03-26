from django.db import models
from budget.models import Item

class Subject(models.Model):
    # Kind Choices
    INCOME = 'I'
    EXPENSE = 'E'
    KIND_CHOICES = (
        (INCOME, '期入'),
        (EXPENSE, '期出')
    )

    book = models.ForeignKey('budget.models.Book')
    name = models.CharField(max_length=16)
    kind = models.CharField(max_length=1, choices=KIND_CHOICES)

    @property
    def estimated_amount(self):
        total = 0
        items = Item.objects.filter(subject=self)
        for it in items:
            total += it.estimated_amount
        return total

    @property
    def actual_amount(self):
        total = 0
        items = Item.objects.filter(subject=self)
        for it in items:
            total += it.actual_amount
        return total
