from django.db import models
from django.utils import timezone

class Advance(models.Model):
    item = models.ForeignKey('budget.Item')
    requirement = models.ForeignKey('core.Requirement')

    amount = models.PositiveIntegerField()
    memo = models.TextField()

    activity_date = models.DateField()

    f_staff_verify = models.NullBooleanField(default=None)
    f_staff_reject_reason = models.TextField()

    f_chief_verify = models.NullBooleanField(default=None)
    f_chief_reject_reason = models.TextField()

    is_balanced = models.BooleanField(default=False)

    @property
    def is_complete(self):
        now = timezone.now()
        if now.date() > self.activity_date:
            if self.receipt_set.exists() and self.is_balanced:
                return True
            else:
                return False
        else:
            return True

    def cite(self):
        advance = Advance.objects.create(
            item=self.item,
            requirement=self.requirement,
            amount=self.amount,
            memo=self.memo,
            activity_date=self.activity_date
        )
        return advance
