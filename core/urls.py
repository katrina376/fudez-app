from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from core.views import AdvanceRequirementViewSet, RegularRequirementViewSet, FundViewSet, ExpenseRecordViewSet


router = DefaultRouter()
router.register(
    r'expenses', ExpenseRecordViewSet, base_name='expense')
router.register(
    r'requirements/advances',
    AdvanceRequirementViewSet, base_name='advance')
router.register(
    r'requirements/regulars',
    RegularRequirementViewSet, base_name='regular')

router.register(
    r'requirements/advances/(?P<requirement_pk>.+)/funds',
    FundViewSet, base_name='advance-fund')
router.register(
    r'requirements/regulars/(?P<requirement_pk>.+)/funds',
    FundViewSet, base_name='regular-fund')

urlpatterns = [
    url(r'^', include(router.urls)),
]
