from django.db import models


class SubjectQuerySet(models.QuerySet):
    def income(self):
        return self.filter(kind=Subject.INCOME)

    def expense(self):
        return self.filter(kind=Subject.EXPENSE)


class Subject(models.Model):
    # Kind Choices
    INCOME = 'I'
    EXPENSE = 'E'
    KIND_CHOICES = (
        (INCOME, '收入'),
        (EXPENSE, '支出'),
    )

    project = models.ForeignKey(
        'Project', on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=16)
    kind = models.CharField(max_length=1, choices=KIND_CHOICES)

    is_reserves = models.BooleanField(default=False)

    objects = SubjectQuerySet.as_manager()

    @property
    def estimated_amount(self):
        return self.items.aggregate(total=models.Sum('estimated_amount'))['total']

    @property
    def actual_amount(self):
        return sum(item.actual_amount for item in self.items.all())
