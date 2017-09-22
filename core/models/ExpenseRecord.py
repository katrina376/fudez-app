from django.db import models

class ExpenseRecord(models.Model):
    # Kind Choices
    INCOME = 'I'
    EXPENSE = 'E'
    KIND_CHOICES = (
        (INCOME, '收入'),
        (EXPENSE, '支出')
    )

    requirement = models.ForeignKey('core.Requirement', primary_key=True, related_name='expense_records')
    kind = models.CharField(max_length=1, choices=KIND_CHOICES)

    memo = models.TextField()
    date = models.DateField(null=True)
    amount = models.PositiveIntegerField(default=0)
