from django.db import models

class UnlockRecord(models.Model):
    department = models.ForeignKey('account.Department', name='unlock_record')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reason = models.TextField()

    def __str__(self):
        return '{} {}-{}'.format(self.department, start_time, end_time)
