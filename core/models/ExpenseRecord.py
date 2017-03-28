from django.db import models

class ExpenseRecord(models.Model):
    department = models.ForeignKey('account.Department')
    memo = models.TextField()
    remit_date = models.DateField()
    income = models.PositiveIntegerField(default=0)
    expense = models.PositiveIntegerField(default=0)
    balance = models.PositiveIntegerField(default=0)

    # TODO: Bind with Requirements

    def __str__(self):
        return '{} {}'.format(self.remit_date, self.balance)
