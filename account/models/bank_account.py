from django.db import models


class BankAccount(models.Model):
    department = models.ForeignKey(
        'Department',
        on_delete=models.PROTECT,
        related_name='bank_accounts'
    )

    bank_name = models.CharField(max_length=10)
    bank_code = models.CharField(max_length=4)
    branch_name = models.CharField(max_length=5)
    account = models.CharField(max_length=20)
    account_name = models.CharField(max_length=16)

    def __str__(self):
        return '{} {}'.format(self.department, self.account_name)
