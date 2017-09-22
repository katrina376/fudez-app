from django.db import models
from core.models import Requirement

class Item(models.Model):
    subject = models.ForeignKey('budget.Subject', related_name='items')

    name = models.CharField(max_length=32)
    estimated_amount = models.PositiveIntegerField(null=True)
    memo = models.TextField()
    addition = models.TextField()

    @property
    def actual_amount(self):
        return sum(fund.amount for fund in self.funds)

    @property
    def efficiency(self):
        return float(self.actual_amount / self.estimated_amount) * 100

    @property
    def report(self):
        return '\n'.join(fund.memo for fund in self.funds)
