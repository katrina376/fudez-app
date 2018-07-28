from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import AdvanceRequirement, RegularRequirement

from .fund import FullFundSerializer
from account.serializers import UserSerializer


class AdvanceRequirementSerializer(serializers.ModelSerializer):
    memo = serializers.CharField(allow_blank=True)
    bank_name = serializers.CharField(allow_blank=True)
    bank_code = serializers.CharField(allow_blank=True)
    branch_name = serializers.CharField(allow_blank=True)
    account = serializers.CharField(allow_blank=True)
    account_name = serializers.CharField(allow_blank=True)
    applicant = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = AdvanceRequirement
        fields = (
            'id',
            'applicant',
            'memo',
            'activity_date',
            'bank_name',
            'bank_code',
            'branch_name',
            'account',
            'account_name',
        )


class SimpleAdvanceRequirementSerializer(serializers.ModelSerializer):
    applicant = UserSerializer()
    state = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = AdvanceRequirement
        fields = (
            'id', 'applicant', 'department', 'state', 'progress',
            'serial_number', 'memo', 'activity_date', 'amount',
            'require_president', 'staff_verify', 'chief_verify',
            'president_verify',
        )
        read_only_fields = fields

    def get_state(self, obj):
        translate = dict(self.Meta.model.STATE_CHOICES)
        return translate[obj.state]

    def get_progress(self, obj):
        translate = dict(self.Meta.model.PROGRESS_CHOICES)
        if obj.progress not in translate:
            return ''
        else:
            return translate[obj.progress]

    def get_department(self, obj):
        return obj.department.name


class FullAdvanceRequirementSerializer(SimpleAdvanceRequirementSerializer):
    department = serializers.SerializerMethodField()
    funds = FullFundSerializer(many=True, read_only=True)

    class Meta:
        model = AdvanceRequirement
        fields = (
            'id', 'applicant', 'department', 'state', 'serial_number',
            'progress', 'memo', 'activity_date', 'amount', 'is_submitted',
            'create_time', 'edit_time', 'submit_time', 'finalize_time',
            'bank_name', 'bank_code', 'branch_name', 'account', 'account_name',
            'staff_verify', 'staff_verify_time', 'staff_reject_reason',
            'chief_verify', 'chief_verify_time', 'chief_reject_reason',
            'require_president', 'president_verify', 'president_verify_time',
            'president_approve_reserves', 'president_reject_reason',
            'funds',
        )

        read_only_fields = fields

    def get_department(self, obj):
        return obj.department.name


class RegularRequirementSerializer(AdvanceRequirementSerializer):
    class Meta:
        model = RegularRequirement
        fields = (
            'id',
            'applicant',
            'memo',
            'activity_date',
            'bank_name',
            'bank_code',
            'branch_name',
            'account',
            'account_name',
            'receipt',
            'advance',
        )


class SimpleRegularRequirementSerializer(SimpleAdvanceRequirementSerializer):
    class Meta:
        model = RegularRequirement
        fields = (
            'id', 'applicant', 'department', 'state', 'progress',
            'serial_number', 'memo', 'activity_date', 'amount',
            'require_president', 'staff_verify', 'chief_verify',
            'president_verify', 'receipt', 'advance',
        )
        read_only_fields = fields


class FullRegularRequirementSerializer(FullAdvanceRequirementSerializer):
    class Meta:
        model = RegularRequirement
        fields = (
            'id', 'applicant', 'department', 'state', 'serial_number',
            'progress', 'memo', 'activity_date', 'amount', 'is_submitted',
            'create_time', 'edit_time', 'submit_time', 'finalize_time',
            'bank_name', 'bank_code', 'branch_name', 'account', 'account_name',
            'staff_verify', 'staff_verify_time', 'staff_reject_reason',
            'chief_verify', 'chief_verify_time', 'chief_reject_reason',
            'require_president', 'president_verify', 'president_verify_time',
            'president_approve_reserves', 'president_reject_reason',
            'funds', 'receipt', 'advance',
        )

        read_only_fields = fields
