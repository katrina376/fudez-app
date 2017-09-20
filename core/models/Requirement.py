import os
from datetime.datetime import timestamp

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

from account.models import User

def file_path(instance, filename):
    ts = int(timestamp(timezone.now()))
    path = 'upload/'
    name = '{}_{}'.format(str(ts), filename)
    return os.path.join(path, name)

class RequirementManager(models.Manager):
    def _add_bank_info(instance, bank_name, bank_code, branch_name, account, account_name):
        instance.bank_name = bank_name
        instance.bank_code = bank_code
        instance.branch_name = branch_name
        instance.account = account
        instance.account_name = account_name
        instance.save()
        return instance

    def _attach_receipt(instance, receipt, require_president):
        instance.receipt = receipt
        instance.require_president = require_president
        instance.save()
        return instance

    def create_requirement(self, applicant, kind, activity_date, memo,
                           advance=None,
                           bank_name='', bank_code='', branch_name='', account='', account_name='',
                           receipt=None, require_president=False):
        requirement = self.create(applicant=applicant, kind=kind ,activity_date=activity_date, memo=memo)

        if kind == Requirement.REIMBURSE:
            requirement = _attach_receipt(requirement, receipt, require_president)
            if advance is None:
                # Regular case
                requirement = _add_bank_info(requirement, bank_name, bank_code, branch_name, account, account_name)
            else:
                # After Advance
                requirement.advance = advance
        elif kind == Requirement.ADVANCE:
            # Advance
            requirement = _add_bank_info(requirement, bank_name, bank_code, branch_name, account, account_name)

        requirement.save()
        return requirement

class Requirement(models.Model):
    # Kind Choices
    ADVANCE = 'A'
    REIMBURSE = 'R'
    KIND_CHOICES = (
        (ADVANCE, '預先請款'),
        (REIMBURSE, '已有收據')
    )

    # State Choices
    DRAFT = 'D'
    SUBMITTED = 'S'
    COMPLETE = 'C'
    ABANDONED = 'A'
    STATE_CHOICES = (
        (DRAFT, '草稿'),
        (SUBMITTED, '提交'),
        (COMPLETE, '完成'),
        (ABANDONED, '失敗')
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

    # General fields for all kinds of requirement
    applicant = models.ForeignKey('account.User')
    serial_number = models.CharField(max_length=12)

    kind = models.CharField(max_length=1, choices=KIND_CHOICES)
    activity_date = models.DateTimeField(null=True)
    memo = models.TextField()

    create_time = models.DateTimeField(auto_now_add=True)
    edit_time = models.DateTimeField(null=True)
    submit_time = models.DateTimeField(null=True)
    finalize_time = models.DateTimeField(null=True)

    staff_verify = models.NullBooleanField(default=None)
    staff_verify_time = models.DateTimeField(null=True)
    staff_reject_reason = models.TextField()

    chief_verify = models.NullBooleanField(default=None)
    chief_verify_time = models.DateTimeField(null=True)
    chief_reject_reason = models.TextField()

    # For cases using reserves (require_president = True)
    president_verify = models.NullBooleanField(default=None)
    president_verify_amount = models.PositiveIntegerField(null=True)
    president_verify_time = models.DateTimeField(null=True)
    president_reject_reason = models.TextField()

    # For advances and regular cases
    bank_name = models.CharField(max_length=10)
    bank_code = models.CharField(max_length=4)
    branch_name = models.CharField(max_length=5)
    account = models.CharField(max_length=20)
    account_name = models.CharField(max_length=12)

    # For reimburses after advances
    advance = models.ForeignKey('core.Requirement')
    is_balanced = models.BooleanField(default=False)

    # For regular cases and reimburses after advances
    receipt = models.FileField(upload_to=file_path)
    require_president = models.BooleanField(default=False)

    objects = RequirementManager()

    @property
    def pay_date(self):
        try:
            return self.expenserecord.remit_date
        except ObjectDoesNotExist:
            return None

    @property
    def progress(self):
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
                if self.advance.is_balanced and self.receipt:
                    return IN_PROGRESS
                elif self.advance.is_balanced:
                    return NO_RECEIPT
                elif self.receipt:
                    return BALANCE_OVERDUE
                else:
                    return NO_RECEIPT_AND_BALANCE_OVERDUE
            return None

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
        # Create serial_number = yyyymmdd + dep_id[dd]+ no[dd]
        now = timezone.now()
        year = now.year
        month = now.month
        day = now.day

        # department
        dep = applicant.department
        # count of the requirements
        count = Requirement.objects.filter(applicant__department=dep).count()

        self.serial_number = str('{:4d}{:2d}{:2d}{:2d}{:2d}'.format(year, month, day, dep.id, count))

        self.state = SUBMITTED
        self.submit_time = now
        self.save()
        return self

    def approve(self, reviewer, amount=0):
        if self.state == SUBMITTED:
            if reviewer.kind == User.STAFF:
                self.staff_verify = True
                self.staff_verify_time = timezone.now()
            elif reviewer.kind == User.CHEIF:
                self.chief_verify = True
                self.chief_verify_time = timezone.now()
            elif (reviewer.kind == User.PRESIDENT) and (self.require_president):
                self.president_verify = True
                self.president_verify_time = timezone.now()
                self.president_verify_amount = amount
            else:
                raise ValueError('User kind is not valid: {}'.format(reviewer.get_kind_display()))
        else:
            raise ValueError('Requirement cannot be reviewed: {}'.format(self.id))

        # Close up after all required reviews are complete
        if self.staff_verify and self.chief_verify:
            if self.require_president:
                if self.president_verify:
                    self.finalize_time = timezone.now()
                    self.state = COMPLETE
            else:
                self.finalize_time = timezone.now()
                self.state = COMPLETE

        self.save()
        return self

    def reject(self, reviewer, reason=''):
        if self.state == SUBMITTED:
            self.state = ABANDONED
            self.finalize_time = timezone.now()
            if reviewer.kind == User.STAFF:
                self.staff_verify = False
                self.staff_verify_time = timezone.now()
                self.staff_reject_reason = reason
            elif reviewer.kind == User.CHIEF:
                self.chief_verify = False
                self.chief_verify_time = timezone.now()
                self.chief_reject_reason = reason
            elif reviewer.kind == User.PRESIDENT:
                self.president_verify = False
                self.president_verify_time = timezone.now()
                self.president_reject_reason = reason
            else:
                raise ValueError('User kind is not valid: {}'.format(reviewer.get_kind_display()))
        else:
            raise ValueError('Requirement cannot be reviewed: {}'.format(self.id))

        self.save()
        return self

    def __str__(self):
        return 'Requirement: Unique ID {0}, serial number {1}'.format(str(self.id),str(self.serial_number))
