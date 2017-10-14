from django.db import models

class FundQuerySet(models.QuerySet):
    def approved(self):
        return self.filter(status=Fund.NORMAL, requirement__state=Requirement.COMPLETE)

class FundManager(models.Maneger):
    def get_queryset(self):
        return FundQuerySet(self.model, using=self._db)

    def approved(self):
        return self.get_queryset().approved()

class Fund(models.Model):
    item = models.ForeignKey('budget.Item', related_name='funds')
    requirement = models.ForeignKey('core.Requirement', related_name='funds')

    amount = models.PositiveIntegerField()
    memo = models.TextField()

    objects = FundManager()
