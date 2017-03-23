from django.db import models

class AdvanceManager(models.Manager):
    def open(item, requirement, amount, memo, activity_date):
        advance = self.create(
            item=item,
            requirement=requirment,
            amount=amount,
            memo=memo,
            activity_date=activity_date
        )
        return advance

class Advance(models.Model):
    item = models.ForeignKey('.models.Item')
    # TODO: Finish the budget models
    requirement = models.ForeignKey('core.models.Requirement')

    amount = models.PositiveIntegerField()
    memo = models.TextField()

    activity_date = models.DateField()

    balanced = models.NullBooleanField(default=null)

    objects = AdvanceManager()

    def balance(self):
        if (self.balanced is False)
            self.balanced = True
        self.save()
        return self
