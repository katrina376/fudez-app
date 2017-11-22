from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from account.views import UserViewSet, DepartmentViewSet, BankAccountViewSet, UnlockRecordViewSet, MeView
from rest_framework_nested import routers

router = DefaultRouter()
router.register(r'users', UserViewSet, base_name='user')
router.register(r'departments', DepartmentViewSet, base_name='department')

departments_router = routers.NestedSimpleRouter(router, r'departments', lookup='department')
departments_router.register(r'accounts', BankAccountViewSet, base_name='department-account')
departments_router.register(r'records', UnlockRecordViewSet, base_name='department-record')

urlpatterns = [
    url(r'^users/me', MeView.as_view()),
    url(r'^', include(router.urls)),
    url(r'^', include(departments_router.urls)),
]
