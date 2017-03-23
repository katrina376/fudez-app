from django.db import models
from core.models import Requirement

class AdvanceManager(models.Manager):
    def open(item, requirement, amount, memo, activity_date):
        advance = self.create(item, requirement, amount, memo, activity_date)
        return advance

class Advance(models.Model):
    item = models.ForeignKey(Item)
    requirement = models.ForeignKey(Requirement)

    amount = models.PositiveIntegerField()
    memo = models.TextField()

    activity_date = models.DateField()

    balanced = models.NullBooleanField(default=null)

    objects = AdvanceManager

    def balance(self):
        if (self.balanced is False)
            self.balanced = True
        self.save()
        return self
