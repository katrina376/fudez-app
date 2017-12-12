from django.contrib import admin
from core.models import AdvanceRequirement, ExpenseRecord, Fund, RegularRequirement

admin.site.register(ExpenseRecord)
admin.site.register(Fund)
admin.site.register(AdvanceRequirement)
admin.site.register(RegularRequirement)
