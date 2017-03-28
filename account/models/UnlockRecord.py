from django.db import models

class UnlockRecord(models.Model):
    department = models.ForeignKey('account.models.Department')
    start_time = DateTimeField()
    end_time = DateTimeField()
    reason = TextField()

    def __str__(self):
        return '{} {}-{}'.format(self.department, start_time, end_time)
