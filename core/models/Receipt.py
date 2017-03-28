import os
from django.conf import settings
from django.db import models
from django.utils import timezone

def file_path(instance, filename):
    path = 'draft/'
    name = '{}_{}_{}'.format(timezone.now(), instance.id, filename)
    return os.path.join(path, name)

class Receipt(models.Model):
    item = models.ForeignKey('budget.Item')
    requirement = models.ForeignKey('core.Requirement')
    advance = models.ForeignKey('core.Advance', null=True)

    amount = models.PositiveIntegerField()
    memo = models.TextField()
    file = models.FileField(upload_to=file_path, max_length=100)

    @property
    def kind(self):
        return self.requirement.kind

    def submit(self):
        serial_number = self.requirement.serial_number
        initial_path = self.file.path
        self.file.name = '{}/{}'.format(serial_number, self.file.name)
        new_path = settings.MEDIA_ROOT + self.file.name
        os.rename(initial_path, new_path)
        self.save()
        return self

    def cite(self, requirement, advance):
        os.copy
        receipt = Receipt.objects.create(
            item=self.item,
            requirement=requirement,
            advance=advance,
            amount=self.amount,
            memo=self.memo,
            file=file
        )
        return receipt

    def __str__(self):
        return 'Receipt: Unique ID {0}, File name {1}'.format(str(self.id), self.file.name)
