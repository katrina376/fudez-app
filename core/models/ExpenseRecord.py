from django.db import models

class ExpenseRecord(models.Model):
    department = ForeignKey('account.models.department')
    memo = TextField()
    remit_date = DateField()
    income = PositiveIntegerField(default=0)
    expense = PositiveIntegerField(default=0)
    balance = PositiveIntegerField(default=0)
    
    # TODO: Bind with Requirements

    def __str__(self):
        return '{} {}'.format(self.remit_date, self.balance)
