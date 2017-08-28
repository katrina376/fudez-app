from django.db import models

class ExpenseRecord(models.Model):
    requirement = models.OneToOneField('core.Requirement', primary_key=True)

    serial_number = models.CharField(max_length=8)
    memo = models.TextField()
    remit_date = models.DateField(null=True)
    income = models.PositiveIntegerField(default=0)
    expense = models.PositiveIntegerField(default=0)

    @property
    def balance(self):
        return 0

    def __str__(self):
        return '{} {}'.format(self.remit_date, self.balance)
