from django.db import models


class Book(models.Model):
    session = models.ForeignKey(
        'Session', on_delete=models.CASCADE, related_name='books')

    name = models.CharField(max_length=32)
    description = models.TextField()

    is_active = models.BooleanField(default=True)
    announce_date = models.DateField()

    @property
    def departments(self):
        return [prj.department for prj in self.projects.all()]

    @property
    def estimated_income(self):
        return sum(project.estimated_income for project in self.projects.all())

    @property
    def estimated_expense(self):
        return sum(project.estimated_expense for project in self.projects.all())

    @property
    def actual_income(self):
        return sum(project.actual_income for project in self.projects.all())

    @property
    def actual_expense(self):
        return sum(project.actual_expense for project in self.projects.all())
