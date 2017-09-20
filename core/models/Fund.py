from django.db import models

class Fund(models.Model):
    item = models.ForeignKey('budget.Item', related_name='funds')
    requirement = models.ForeignKey('core.Requirement', related_name='funds')

    amount = models.PositiveIntegerField()
    memo = models.TextField()
