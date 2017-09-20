from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import Requirement

class Department(models.Model):
    # Kind Choices
    EXECUTIVE = 'E'
    LEGISLATIVE = 'L'
    JUDICIAL = 'J'
    KIND_CHOICES = (
        (EXECUTIVE, '行政部門'),
        (LEGISLATIVE, '立法部門'),
        (JUDICIAL, '司法部門')
    )

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=16)
    kind = models.CharField(max_length=1, choices=KIND_CHOICES)
    assistant = models.ForeignKey('account.User', null=True, related_name='+',)

    @property
    def is_locked(self):
        res = False

        # Check advance requirements
        advances = Requirement.objects.filter(applicant__department=self)
        for a in advances:
            if not a.is_complete:
                res = True
                break

        # Check UnlockRecord
        now = timezone.now()
        if self.unlockrecord_set.filter(start_time__lt=now, end_time__gt=now).exists():
            res = False

        return res

    def __str__(self):
        return self.name
