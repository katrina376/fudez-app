from django.db import models
from core.models import Receipt

class Item(models.Model):
    subject = models.ForeignKey('budget.models.Subject')

    name = models.CharField(max_length=32)
    estimated_amount = models.PositiveIntegerField(null=True)
    memo = models.TextField()

    @property
    def actual_amount(self):
        total = 0
        receipts = Receipts.objects.filter(item=self)
        for r in receipts:
            total += r.amount
        return total

    # TODO: Combine all receipts' memo
