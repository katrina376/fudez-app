from django.db import models

class Book(models.Model):
    session = models.ForeignKey('budget.Session')

    title = models.CharField(max_length=32)
    description = models.TextField()

    is_active = models.BooleanField(default=True)
    announce_date = models.DateField()

    @property
    def estimated_amount(self):
        total = 0
        projects = self.project_set.all()
        for prj in projects:
            total += prj.estimated_amount
        return total

    @property
    def actual_amount(self):
        total = 0
        projects = self.project_set.all()
        for prj in projects:
            total += prj.actual_amount
        return total
