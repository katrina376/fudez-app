from django.db import models
from core.models import Requirement

class Receipt(models.Model):
    item = models.ForeignKey(Item)
    Requirement = models.ForeignKey(Requirement)

    # TODO: How to merge with the advances?

    amount = models.PositiveIntegerField()
    memo = models.TextField(blank=True)
    file = models.FileField(upload_to='uploads/draft/', max_length=100)

    @classmethod
    def upload(cls, item, requirement, ammout, memo, file):
        receipt = cls(
            item=item,
            requirement=requirement,
            ammout=ammout,
            memo=memo,
            file=file
        )
        # TODO: Set file name
        receipt.save()
        return receipt

    def submit(self):
        # TODO: Set file name => uploads/{serial_number}/{self.id}

    def __str__(self):
        return 'Receipt: Unique ID {0}, File name {1}'.format(str(self.id), self.file.name)
