from django.db import models

class Subject(models.Model):
    # Kind Choices
    INCOME = 'I'
    EXPENSE = 'E'
    KIND_CHOICES = (
        (INCOME, '收入'),
        (EXPENSE, '支出')
    )

    project = models.ForeignKey('budget.Project', related_name='subjects')
    name = models.CharField(max_length=16)
    kind = models.CharField(max_length=1, choices=KIND_CHOICES)

    @property
    def estimated_amount(self):
        return self.items.aggregate(models.Sum('estimated_amount'))

    @property
    def actual_amount(self):
        return sum(item.actual_amount for item in self.items.all())
