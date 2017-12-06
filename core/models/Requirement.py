import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone

from core.models import Fund


def file_path(instance, filename):
    ts = int(datetime.timestamp(timezone.now()))
    path = 'upload/'
    name = '{}_{}'.format(str(ts), filename)
    return os.path.join(path, name)


class RequirementQuerySet(models.QuerySet):
    def advance(self):
        return self.filter(regularrequirement__isnull=True)

    def regular(self):
        return self.filter(regularrequirement__isnull=False)


class Requirement(models.Model):
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
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    serial_number = models.CharField(max_length=12)

    activity_date = models.DateTimeField(null=True)
    memo = models.TextField()

    is_submitted = models.BooleanField(default=False)

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

    # For cases that require_president = True
    president_verify = models.NullBooleanField(default=None)
    president_approve_reserves = models.OneToOneField('core.Fund', on_delete=models.CASCADE, null=True, related_name='approve_reserves')
    president_verify_time = models.DateTimeField(null=True)
    president_reject_reason = models.TextField()

    bank_name = models.CharField(max_length=10)
    bank_code = models.CharField(max_length=4)
    branch_name = models.CharField(max_length=5)
    account = models.CharField(max_length=20)
    account_name = models.CharField(max_length=12)

    objects = RequirementQuerySet.as_manager()

    @property
    def department(self):
        return self.applicant.department

    @property
    def amount(self):
        total = self.funds.normal().aggregate(total=models.Sum('amount'))['total']
        return 0 if total is None else total

    @property
    def require_president(self):
        if self.amount >= 10000 or self.funds.filter(item__subject__is_reserves=True).exists():
            return True
        else:
            return False

    @property
    def state(self):
        if not self.is_submitted:
            return self.DRAFT
        else:
            verify_states = [self.staff_verify, self.chief_verify, self.president_verify]
            if any(verify is False for verify in verify_states):
                return self.ABANDONED
            elif all(verify is True for verify in verify_states[0:1]):
                if self.require_president and verify_states[2] is True:
                    return self.COMPLETE
                else:
                    return self.SUBMITTED
            else:
                return self.SUBMITTED

    @property
    def progress(self):
        return None

    def edit(self, edit_dict):
        if not isinstance(edit_dict, dict):
            raise TypeError('Input is not a dictionary')
        if self.state == self.DRAFT:
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
        dep = self.applicant.department
        # count of the requirements
        count = Requirement.objects.filter(applicant__department=dep).count()

        self.serial_number = str('{:04d}{:02d}{:02d}{:02d}{:02d}'.format(year, month, day, dep.id, count))

        self.is_submitted = True
        self.submit_time = now
        self.save()
        return self

    def approve(self, reviewer, amount=0):
        try:
            amount = int(amount)
        except:
            raise TypeError('Input amount type error: {}'.format(type(amount)))

        if self.is_submitted:
            if reviewer.kind == get_user_model().STAFF:
                self.staff_verify = True
                self.staff_verify_time = timezone.now()
            elif reviewer.kind == get_user_model().CHIEF:
                self.chief_verify = True
                self.chief_verify_time = timezone.now()
            elif (reviewer.kind == get_user_model().PRESIDENT) and (self.require_president):
                self.president_verify = True
                self.president_verify_time = timezone.now()
                self.president_approve_reserves = Fund.objects.approve_reserves(amount=amount, requirement=self)
            else:
                raise ValueError('User kind is not valid: {}'.format(reviewer.get_kind_display()))
        else:
            raise ValueError('Requirement cannot be reviewed: {}'.format(self.id))

        # Close up after all required reviews are complete
        if self.staff_verify and self.chief_verify:
            if self.require_president:
                if self.president_verify:
                    self.finalize_time = timezone.now()
            else:
                self.finalize_time = timezone.now()

        self.save()
        return self

    def reject(self, reviewer, reason=''):
        if self.state == SUBMITTED:
            self.state = ABANDONED
            self.finalize_time = timezone.now()
            if reviewer.kind == get_user_model().STAFF:
                self.staff_verify = False
                self.staff_verify_time = timezone.now()
                self.staff_reject_reason = reason
            elif reviewer.kind == get_user_model().CHIEF:
                self.chief_verify = False
                self.chief_verify_time = timezone.now()
                self.chief_reject_reason = reason
            elif reviewer.kind == get_user_model().PRESIDENT:
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
        return 'Unique ID {0}, serial number {1}'.format(str(self.id),str(self.serial_number))


class AdvanceRequirement(Requirement):
    class Meta:
        proxy = True

    @property
    def is_balanced(self):
        expense_amount = self.expense_records.expense().aggregate(models.SUM('amount'))['amount__sum']
        return_amount = self.expense_records.income().aggregate(models.SUM('amount'))['amount__sum']
        expense_sum = expense_amount - return_amount

        reimburse_amount = Fund.objects.filter(requirement__in=self.reimburses).aggregate(models.SUM('amount'))['amount__sum']

        return expense_sum == self.amount - reimburse_amount

    @property
    def progress(self):
        if self.state == self.DRAFT:
            return None
        else:
            if self.reimburses.is_balanced and self.receipt:
                return self.IN_PROGRESS
            elif self.advance.is_balanced:
                return self.NO_RECEIPT
            elif self.receipt:
                return self.BALANCE_OVERDUE
            else:
                return self.NO_RECEIPT_AND_BALANCE_OVERDUE


class RegularRequirement(Requirement):
    advance = models.ForeignKey('core.Requirement', on_delete=models.SET_NULL, related_name='reimburses', null=True)

    receipt = models.FileField(upload_to=file_path)

    @property
    def progress(self):
        if self.state == self.DRAFT:
            return None
        else:
            if self.state == self.COMPLETE:
                return self.CLOSE_UP
            elif self.state == self.ABANDONED:
                return self.REJECT
            else:
                return self.IN_PROGRESS
