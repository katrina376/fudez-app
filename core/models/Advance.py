from django.db import models
from core.models import Requirement

class Advance(models.Model):
    item = models.ForeignKey(Item)
    requirement = models.ForeignKey(Requirement)

    amount = models.PositiveIntegerField()
    memo = models.TextField()

    activity_date = models.DateField()

    balanced = models.BooleanField()

    @classmethod
    def open(cls, item, requirement, amount, memo, activity_date):
        advance = cls(
            item=item,
            requirement=requirement,
            amount=amount,
            memo=memo,
            activity_date=activity_date
        )
        return advance

    def balance(self):
        if (self.balanced is False)
            self.balanced = True
        self.save()
        return self
