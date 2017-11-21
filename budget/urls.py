from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from budget.views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, base_name='book')

urlpatterns = [
     url(r'^', include(router.urls))
]
