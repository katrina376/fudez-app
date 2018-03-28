from django.apps import apps
from django.conf import settings
from django.db import models
from django.utils import timezone


class Department(models.Model):
    # Kind Choices
    EXECUTIVE = 'E'
    LEGISLATIVE = 'L'
    JUDICIAL = 'J'
    KIND_CHOICES = (
        (EXECUTIVE, '行政部門'),
        (LEGISLATIVE, '立法部門'),
        (JUDICIAL, '司法部門'),
    )

    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=16, default='暫存')
    kind = models.CharField(
        max_length=1, choices=KIND_CHOICES, default=EXECUTIVE)
    assistant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, related_name='assist_departments')

    @property
    def is_locked(self):
        res = False

        # Check advance requirements
        advances = apps.get_model('core.AdvanceRequirement').objects.filter(
            applicant__department=self)
        for a in advances:
            if not a.is_complete:
                res = True
                break

        # Check UnlockRecord
        now = timezone.now()
        if self.unlock_records.filter(start_time__lt=now, end_time__gt=now).exists():
            res = False

        return res

    def __str__(self):
        return self.name
