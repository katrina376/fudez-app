from django.db import models

class ReceiptManager(models.Manager):
    def upload(self, item, requirement, ammout, memo, file):
        receipt = self.create(
            item=item,
            requirement=requirement,
            ammout=ammout,
            memo=memo,
            file=file
        )
        # TODO: Set file name
        return receipt

class Receipt(models.Model):
    item = models.ForeignKey('.models.Item')
    # TODO: Finish the budget models
    Requirement = models.ForeignKey('core.models.Requirement')

    # TODO: How to merge with the advances?

    amount = models.PositiveIntegerField()
    memo = models.TextField()
    file = models.FileField(upload_to='uploads/draft/', max_length=100)

    objects = ReceiptManager()

    def submit(self):
        # TODO: Set file name => uploads/{serial_number}/{self.id}

    def __str__(self):
        return 'Receipt: Unique ID {0}, File name {1}'.format(str(self.id), self.file.name)
