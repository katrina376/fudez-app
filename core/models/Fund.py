from django.db import models

class FundQuerySet(models.QuerySet):
    def normal(self):
        return self.filter(status=Fund.NORMAL)

    def approved(self):
        funds = self.filter(status=Fund.NORMAL, requirement__regularrequirement__isnull=False)
        pk_list = [fund.pk for fund in funds if fund.requirement.state == fund.requirement.COMPLETE]
        return self.filter(pk__in=pk_list)

class FundManager(models.Manager):
    def get_queryset(self):
        return FundQuerySet(self.model, using=self._db)

    def normal(self):
        return self.get_queryset().normal()

    def approved(self):
        return self.get_queryset().approved()

    def approve_reserves(self, amount, requirement):
        if requirement.funds.filter(item__subject__is_reserves=True).exists():
            original_fund = requirement.funds.get(item__subject__is_reserves=True)
            item = original_fund.item
            fund = self.create(item=item, requirement=requirement, amount=amount, reserves=original_fund)
            original_fund.status = self.model.DEPRECATED
            original_fund.save()
            return fund
        else:
            return None

class Fund(models.Model):
    # Status Choices
    NORMAL = 'N'
    DEPRECATED = 'D'
    STATUS_CHOICES = (
        (NORMAL, '正常'),
        (DEPRECATED, '廢棄')
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=NORMAL)

    item = models.ForeignKey('budget.Item', on_delete=models.PROTECT, related_name='funds')
    requirement = models.ForeignKey('core.Requirement', on_delete=models.CASCADE, related_name='funds')

    amount = models.PositiveIntegerField()
    memo = models.TextField()

    objects = FundManager()

    def __str__(self):
        return 'Requirement {} Fund {}'.format(self.requirement.pk, self.id)
