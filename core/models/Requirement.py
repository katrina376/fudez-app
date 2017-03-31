from django.db import models
from django.utils import timezone
from account.models import User

class Requirement(models.Model):
    # Kind Choices
    ADVANCE = 'A'
    REIMBURSE = 'R'
    KIND_CHOICES = (
        (ADVANCE, '預先請款'),
        (REIMBURSE, '已有收據')
    )

    # State Choices
    BLANK = 'B'
    DRAFT = 'D'
    WAIT_D_CHIEF_VERIFY = 'V'
    WAIT_PRESIDENT_VERIFY = 'P'
    WAIT_F_STAFF_VERIFY = 'S'
    WAIT_F_CHIEF_VERIFY = 'F'
    APPROVED = 'A'
    COMPLETE = 'C'
    ABANDONED = 'B'
    STATE_CHOICES = (
        (DRAFT, '草稿'),
        (WAIT_D_CHIEF_VERIFY, '等待部長確認'),
        (WAIT_PRESIDENT_VERIFY, '等待會長確認'),
        (WAIT_F_STAFF_VERIFY, '等待財務部部員審核'),
        (WAIT_F_CHIEF_VERIFY, '等待財務部部長審核'),
        (APPROVED, '審核通過'),
        (COMPLETE, '請款完成'),
        (ABANDONED, '請款失敗')
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

    # TODO: How to recognize the kind of user?

    d_staff = models.ForeignKey('account.User')
    serial_number = models.CharField(max_length=12)

    kind = models.CharField(max_length=1, choices=KIND_CHOICES)

    state = models.CharField(max_length=1, choices=STATE_CHOICES, default=DRAFT)

    bank_code = models.CharField(max_length=4)
    branch_code = models.CharField(max_length=5)
    account = models.CharField(max_length=20)
    account_name = models.CharField(max_length=12)

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(null=True)
    submit_time = models.DateTimeField(null=True)
    finalize_time = models.DateTimeField(null=True)

    d_chief_verify = models.NullBooleanField(default=None)
    d_cheif_verify_time = models.DateTimeField(null=True)

    president_verify = models.NullBooleanField(default=None)
    president_verify_time = models.DateTimeField(null=True)

    f_staff_verify = models.NullBooleanField(default=None)
    f_staff_verify_time = models.DateTimeField(null=True)
    f_staff_reject_reason = models.TextField()

    f_chief_verify = models.NullBooleanField(default=None)
    f_cheif_verify_time = models.DateTimeField(null=True)
    f_chief_reject_reason = models.TextField()

    pay_date = models.DateField(null=True)
    expense = models.ForeignKey('core.ExpenseRecord', null=True)

    @property
    def stage(self):
        if self.state == DRAFT:
            return None
        else:
            if self.kind == REIMBURSE:
                if self.state == COMPLETE:
                    return CLOSE_UP
                elif self.state == ABANDONED:
                    return REJECT
                else:
                    return IN_PROGRESS
            else:
                for a in self.advance_set.all():
                    if a.is_balanced and a.receipt_set.exists():
                        return IN_PROGRESS
                    elif a.is_balanced:
                        return NO_RECEIPT
                    elif receipts.exists():
                        BALANCE_OVERDUE
                    else:
                        return NO_RECEIPT_AND_BALANCE_OVERDUE
                return None

    @property
    def need_president_verify(self):
        # TODO: Set the condition for president to verify
        if ...:
            return True
        else:
            return False

    def edit(self, edit_dict):
        if not isinstance(edit_dict ,dict):
            raise TypeError('Input is not a dictionary')
        if self.state == DRAFT:
            for name, value in edit_dict:
                setattr(self, name, value)
            self.edit_time = timezone.now()
            self.save()
            return self
        else:
            raise Exception('This requirement is not a draft: {}'.format(self.id))

    def submit(self):
        # id = yyyymmdd + dep_id[dd]+ no[dd]
        now = timezone.now()
        year = now.year
        month = now.month
        day = now.day

        # department
        dep = d_staff.department
        # count of the requirements
        count = Requirement.objects.filter(d_staff__department=dep, submit_time__date=now).count()

        self.serial_number = str('{:4d}{:2d}{:2d}{:2d}{:2d}'.format(year, month, day, dep.id, count))

        self.state = WAIT_D_CHIEF_VERIFY

        self.submit_time = now
        self.save()
        return self

    def cite(self):
        if self.state == ABANDONED:
            requirement = Requirement.objects.create(d_staff=self.d_staff, kind=self.kind)
            requirement.edit({
                'bank_code': self.bank_code,
                'branch_code': self.branch_code,
                'account': self.account,
                'account_name': self.account_name
            })
            requirement.save()
            return requirement
        else:
            raise Exception('Requirement is not abandoned, thus cannot be copied: {}'.format(self.id))

    def approve(self, user):
        if (self.state == WAIT_D_CHIEF_VERIFY) and (user.kind == User.D_CHIEF):
            self.d_chief_verify = True
            self.d_chief_verify_time = timezone.now()
            if self.need_president_verify:
                self.state = WAIT_PRESIDENT_VERIFY
            else:
                self.state = WAIT_F_STAFF_VERIFY
        elif (self.state == WAIT_PRESIDENT_VERIFY) and (user.kind == User.PRESIDENT):
            self.president_verify = True
            self.president_verify_time = timezone.now()
            self.state = WAIT_F_STAFF_VERIFY
        elif (self.state == WAIT_F_STAFF_VERIFY) and (user.kind == User.F_STAFF):
            self.f_staff_verify = True
            self.f_staff_verify_time = timezone.now()
            self.state = WAIT_F_CHIEF_VERIFY
        elif (self.state == WAIT_F_CHIEF_VERIFY) and (user.kind == User.F_CHIEF):
            self.f_chief_verify = True
            self.f_chief_verify_time = timezone.now()
            if self.kind == REIMBURSE:
                self.state = COMPLETE
                self.finalize_time = timezone.now()
        else:
            raise ValueError('Identity is not valid: {}'.format(identity))
        self.save()
        return self

    def reject(self, user, reason=''):
        if (self.state == WAIT_D_CHIEF_VERIFY) and (user.kind == User.D_CHIEF):
            self.d_chief_verify = False
            self.d_chief_verify_time = timezone.now()
        elif (self.state == WAIT_PRESIDENT_VERIFY) and (user.kind == User.PRESIDENT):
            self.president_verify = False
            self.president_verify_time = timezone.now()
        elif (self.state == WAIT_F_STAFF_VERIFY) and (user.kind == User.F_STAFF):
            self.f_staff_verify = False
            self.f_staff_verify_time = timezone.now()
            self.f_staff_reject_reason = reason
        elif (self.state == WAIT_F_CHIEF_VERIFY) and (user.kind == User.F_CHIEF):
            self.f_chief_verify = False
            self.f_chief_verify_time = timezone.now()
            self.f_chief_reject_reason = reason
        else:
            raise ValueError('Identity is not valid: {}'.format(user.get_identity_display()))
        self.state = ABANDONED
        self.finalize_time = timezone.now()
        self.save()
        return self

    def close(self):
        if (self.state == DRAFT):
            self.finalize_time = timezone.now()
            self.save()
            return self
        else:
            raise Exception('Requirement cannot be closed since it was submitted: {}'.format(self.serial_number))

    def __str__(self):
        return 'Requirement: Unique ID {0}, serial number {1}'.format(str(self.id),str(self.serial_number))
