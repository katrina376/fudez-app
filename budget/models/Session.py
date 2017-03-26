from django.db import models

class Session(models.Model):
    name = models.CharField(max_length=16)
    start_date = models.DateField()
    end_date = models.DateField()
