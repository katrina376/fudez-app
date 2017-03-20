from django.db import models
from django.utils import timezone

class Reimbursement(models.Model):
    # Kind Choices
    ADVANCE = 'A'
    REIMBURSE = 'R'
    KIND_CHOICES = (
        (ADVANCE, '預先請款'),
        (REIMBURSE, '已有收據'),
        (EXECUTE, '預先請款執行')
    )

    # State Choices
    EDITABLE = 'E'
    SUBMITTED = 'S'
    STATE_CHOICES = (
        (EDITABLE, '可編輯'),
        (SUBMITTED, '已送出'),
    )

    # Progress Choices
    CLOSE_UP = 'C'
    REJECT = 'R'
    IN_PROGRESS = 'I'
    NO_RECEIPT = 'N'
    BALANCE_OVERDUE = 'B'
    NO_RECEIPT_AND_BALANCE_OVERDUE = 'A'
    PROGRESS_CHOICES = (
        (CLOSE_UP, '報帳完成'),
        (REJECT, '駁回'),
        (IN_PROGRESS, '處理中'),
        (NO_RECEIPT, '欠缺收據'),
        (BALANCE_OVERDUE, '餘款尚未繳回'),
        (NO_RECEIPT_AND_BALANCE_OVERDUE, '欠收據且餘款未繳回')
    )
    # TODO: The state needs to be reformed; wait for Elantris

    user = models.ForeignKey(User)
    serial_number = models.CharField(max_length=12, blank=True)

    kind = models.CharField(max_length=1, choices=KIND_CHOICES)

    editable = models.BooleanField(default=True)
    progress = models.CharField(max_length=1, choices=PROGRESS_CHOICES, blank=True)
    # state = models.CharField(max_length=1, choices=STATE_CHOICES, default=DRAFT)

    bank_code = models.CharField(max_length=4, null=True)
    branch_code = models.CharField(max_length=5, null=True)
    account = models.CharField(max_length=20, null=True)
    account_name = models.CharField(max_length=12, null=True)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(null=True)
    submit_time = models.DateTimeField(null=True)
    finalize_time = models.DateTimeField(null=True)

    department_confirm = models.NullBooleanField(default=null)

    staff_approve = models.NullBooleanField(default=null)
    staff_reject_reason = models.TextField(blank=True)

    chief_approve = models.NullBooleanField()
    chief_reject_reason = models.TextField(blank=True)

    pay_date = models.DateField(null=True)
    expense_id = models.CharField(max_length=10, null=True)

    @classmethod
    def open(cls, user, kind):
        record = cls(
            user=user,
            kind=kind,
        )
        return record

    def edit(self, edit_dict):
        if (self.editable):
            for name, value in edit_dict:
                setattr(self, name, value)
            self.edit_time = timezone.now()
            self.save()
        else:
            raise Exception('This record is not editable: %s', self.id)

    def submit(self):
        # id = yyyymmdd + dep_id[dd]+ no[dd]
        now = timezone.now()
        year = now.year
        month = now.month
        day = now.day

        # department_id
        department = self.user.department
        # count of the records
        count = len(Record.objects.filter(user__department=department).filter(submit_time__date=now)) + 1
        # TODO: catch exception if department and users do not match

        self.serial_number = str('{:4d}{:2d}{:2d}{:2d}{:2d}'.format(year, month, day, department.id, count))

        self.editable = False
        self.progress = IN_PROGRESS

        self.submit_time = now
        self.save()
        return self

    def cite(self):
        if (self.progress is REJECT):
            self.finalize_time = timezone.now()
            self.save()

            record = Record.start(self.user, self.kind)
            record = Record.edit({
                'bank_code': self.bank_code,
                'branch_code': self.branch_code,
                'account': self.account,
                'account_name': self.account_name
            })
            record.save()
            return record
        else:
            raise Exception('Record is not rejected, cannot be copied: %s', self.id)

    # For chief of the department to confirm the record
    def confirm(self):
        self.department_confirm = True
        self.save()
        return self

    # For staff of the dep. of finance to approve, reject and fill in reason
    def approve(self, identity):
        if (identity is '財務部部長'):
            self.chief_approve = True
            self.save()
        elif (identity is '財務部部員'):
            self.staff_review = True
            self.save()
        else:
            raise ValueError('Identity is not valid: %s', identity)
        if (self.kind == REIMBURSE):
            if (self.chief_approve and self.staff_review):
                self.progress = CLOSE_UP
                self.finalize_time = timezone.now()
                self.save()
        return self

    def reject(self, identity, reason):
        if (identity is '財務部部長'):
            self.progress = REJECT
            self.chief_approve = False
            self.chief_reject_reason = reason
            self.save()
        elif (identity is '財務部部員'):
            self.progress = REJECT
            self.staff_approve = False
            self.staff_reject_reason = reason
            self.save()
        else:
            raise ValueError('Identity is not valid: %s', identity)

    def close(self):
        if (self.state is not SUBMITTED):
            self.finalize_time = timezone.now()
            self.save()
        else:
            raise Exception('Record cannot be closed since it was submitted: %s', self.serial_number)

    # For chief of the department of finance to set the pay date
    def set_pay_date(self, date):
        self.pay_date = date
        self.save()
        return self

    def get_pay_date(self):
        return self.pay_date

    # For chief of the department of finance to set the expense id
    def set_expense_id(self, expense_id):
        self.expense_id = expense_id
        self.save()
        return self

    def get_expense_id(self):
        return self.expense_id

    def __str__(self):
        return 'Record: Unique ID {0}, serial number {1}'.format(str(self.id),str(self.serial_number))
