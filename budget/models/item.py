from django.apps import apps
from django.db import models


class Item(models.Model):
    subject = models.ForeignKey(
        'Subject', on_delete=models.CASCADE, related_name='items')

    name = models.CharField(max_length=32)
    estimated_amount = models.PositiveIntegerField(null=True)
    memo = models.TextField()
    addition = models.TextField()

    @property
    def advances(self):
        return apps.get_model('core.Requirement').objects.advances().filter(
            funds__in=self.funds.normal())

    @property
    def regulars(self):
        return apps.get_model('core.Requirement').objects.regulars().filter(
            funds__in=self.funds.normal())

    @property
    def actual_amount(self):
        total = self.funds.approved().aggregate(
            total=models.Sum('amount'))['total']
        return 0 if total is None else total

    @property
    def efficiency(self):
        if self.estimated_amount > 0:
            return float(self.actual_amount / self.estimated_amount) * 100
        else:
            return 0

    @property
    def report(self):
        return '\n'.join([fund.memo for fund in self.funds.approved()])
