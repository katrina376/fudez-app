from django.db import models

class Subject(models.Model):
    # Kind Choices
    INCOME = 'I'
    EXPENSE = 'E'
    KIND_CHOICES = (
        (INCOME, '收入'),
        (EXPENSE, '支出')
    )

    project = models.ForeignKey('budget.Project')
    name = models.CharField(max_length=16)
    kind = models.CharField(max_length=1, choices=KIND_CHOICES)

    @property
    def estimated_amount(self):
        total = 0
        items = self.item_set.all()
        for it in items:
            total += it.estimated_amount
        return total

    @property
    def actual_amount(self):
        total = 0
        items = self.item_set.all()
        for it in items:
            total += it.actual_amount
        return total
