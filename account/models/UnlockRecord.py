from django.db import models

class UnlockRecord(models.Model):
    department = models.ForeignKey('account.Department', related_name='unlock_records')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reason = models.TextField()

    def __str__(self):
        return '{} {}-{}'.format(self.department, start_time, end_time)
