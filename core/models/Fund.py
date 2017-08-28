from django.db import models

class Fund(models.Model):
    item = models.ForeignKey('budget.Item')
    requirement = models.ForeignKey('core.Requirement')

    amount = models.PositiveIntegerField()
    memo = models.TextField()

    def __str__(self):
        return '{} ({})'.format(memo, receipt.file)
