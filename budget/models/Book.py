from django.db import models

class Book(models.Model):
    session = models.ForeignKey('budget.Session', related_name='books')

    name = models.CharField(max_length=32)
    description = models.TextField()

    is_active = models.BooleanField(default=True)
    announce_date = models.DateField()

    @property
    def estimated_income(self):
        total = 0
        projects = self.projects.all()
        for prj in projects:
            total += prj.estimated_income
        return total

    @property
    def estimated_expense(self):
        total = 0
        projects = self.projects.all()
        for prj in projects:
            total += prj.estimated_expense
        return total

    @property
    def actual_income(self):
        total = 0
        projects = self.projects.all()
        for prj in projects:
            total += prj.actual_income
        return total

    @property
    def actual_expense(self):
        total = 0
        projects = self.projects.all()
        for prj in projects:
            total += prj.actual_expense
        return total
