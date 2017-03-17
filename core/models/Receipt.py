from django.db import models

class Receipt(models.Model):
    item = models.ForeignKey(Item)
    record = models.ForeignKey(Record)

    amount = models.PositiveIntegerField()
    memo = models.TextField(blank=True)
    file = models.FileField(upload_to='uploads/', max_length=100)

    @classmethod
    def upload(cls, item, record, ammout, memo, file):
        receipt = cls(
            item=item,
            record=record,
            ammout=ammout,
            memo=memo,
            file=file
        )
        # TODO: Set file name
        return receipt

    def __str__(self):
        return 'Receipt: Unique ID {0}, File name {1}'.format(str(self.id), self.file.name)
