from django.db import models

class Project(models.Model):
    book = models.ForeignKey('budget.Book')
    department = models.ForeignKey('account.Department')
    name = models.CharField(max_length=16)
    kind = models.CharField(max_length=1, choices=KIND_CHOICES)

    @property
    def estimated_amount(self):
        total = 0
        subjects = self.subject_set.all()
        for sub in subjects:
            total += sub.estimated_amount
        return total

    @property
    def actual_amount(self):
        total = 0
        subjects = self.subject_set.all()
        for sub in subjects:
            total += sub.actual_amount
        return total
