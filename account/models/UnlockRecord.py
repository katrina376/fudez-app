from django.db import models

class UnlockRecord(models.Model):
    department = models.ForeignKey('account.models.Department')
    start_time = DateTimeField()
    end_time = DateTimeField()
    reason = TextField()
