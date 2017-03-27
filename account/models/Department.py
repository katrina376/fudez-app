from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from account.models import UnlockRecord
from core.models import Requirement, Advance

def validate_id(value):
    if Department.objects.filter(id=value).exists():
        raise ValidationError(
            _('Department ID already exists: %(value)s'),
            params={'value': value},
            code='invalid'
        )

class Department(models.Model):
    # Kind Choices
    EXECUTIVE = 'E'
    LEGISLATIVE = 'L'
    JUDICIAL = 'J'
    KIND_CHOICES = (
        (EXECUTIVE, '行政部門')
        (LEGISLATIVE, '立法部門')
        (JUDICIAL, '司法部門')
    )

    id = models.IntegerField(primary_key=True, validator=[validate_id])
    name = models.CharField(max_length=16)
    kind = models.CharField(max_length=1, choices=KIND_CHOICES)
    fa = models.ForeignKey('account.models.User', null=True)

    @property
    def is_locked(self):
        res = False

        # Check Advance
        advances = Advance.objects.filter(requirement__user__department=self)
        for a in advances:
            if not a.is_complete:
                res = True
                break

        # Check UnlockRecord
        now = timezone.now()
        if UnlockRecord.objects.filter(department=self, start_time__lt=now, end_time__gt=now).exists():
            res = False

        return res

    def __str__(self):
        return self.name
