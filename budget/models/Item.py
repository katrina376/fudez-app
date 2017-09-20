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
        total = 0
        funds = self.funds.filter(requirement__kind=Requirement.REIMBURSE, requirement__state=Requirement.COMPLETE)
        for f in funds:
            total += f.amount
        return total

    @property
    def efficiency(self):
        return float(self.actual_amount / self.estimated_amount) * 100

    @property
    def report(self):
        funds = self.funds.filter(requirement__kind=Requirement.REIMBURSE, requirement__state=Requirement.COMPLETE)
        return '\n'.join(funds)
