from django.db import models

class FundQuerySet(models.QuerySet):
    def approved(self):
        return self.filter(status=Fund.NORMAL, requirement__state=Requirement.COMPLETE)

class FundManager(models.Maneger):
    def get_queryset(self):
        return FundQuerySet(self.model, using=self._db)

    def approved(self):
        return self.get_queryset().approved()

    def approve_reserves(self, amount, requirement):
        original_fund = requirement.funds.get(item__subject__is_reserves=True)
        item = original_fund.item
        fund = self.create(item=item, requirement=requirement, amount=amount, reserves=original_fund)
        original_fund.status = Fund.DEPRECATED
        original_fund.save()
        return fund

class Fund(models.Model):
    # Status Choices
    NORMAL = 'N'
    DEPRECATED = 'D'
    STATUS_CHOICES = (
        (NORMAL, '正常'),
        (DEPRECATED, '廢棄')
    )

    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=NORMAL)

    item = models.ForeignKey('budget.Item', related_name='funds')
    requirement = models.ForeignKey('core.Requirement', related_name='funds')
    reserves = models.ForeignKey('core.Fund', on_delete=models.CASCADE, null=True, unique=True)

    amount = models.PositiveIntegerField()
    memo = models.TextField()

    objects = FundManager()
