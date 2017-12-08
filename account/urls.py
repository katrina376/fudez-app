from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from account.views import UserViewSet, DepartmentViewSet, BankAccountViewSet, UnlockRecordViewSet, MeView, MeResetPasswordView

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')
router.register(r'departments', DepartmentViewSet, base_name='department')
router.register(r'records', UnlockRecordViewSet, base_name='record')
router.register(
    r'departments/(?P<department_pk>.+)/accounts',
    BankAccountViewSet, base_name='department-account')

urlpatterns = [
    url(r'^users/me/reset-password', MeResetPasswordView.as_view()),
    url(r'^users/me', MeView.as_view()),
    url(r'^', include(router.urls)),
]
