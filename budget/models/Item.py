from django.db import models
from core.models import Requirement

class Item(models.Model):
    subject = models.ForeignKey('budget.Subject', on_delete=models.CASCADE, related_name='items')

    name = models.CharField(max_length=32)
    estimated_amount = models.PositiveIntegerField(null=True)
    memo = models.TextField()
    addition = models.TextField()

    @property
	def advances(self):
        return Requirement.objects.advances().filter(funds__in=self.funds.approved())

	@property
	def reimburses(self):
        return Requirement.objects.reimburses().filter(funds__in=self.funds.approved())

	@property
    def actual_amount(self):
        return self.funds.approved().aggregate(models.Sum('amount'))

    @property
    def efficiency(self):
        return float(self.actual_amount / self.estimated_amount) * 100

    @property
    def report(self):
        return '\n'.join([fund.memo for fund in self.funds.approved()])
