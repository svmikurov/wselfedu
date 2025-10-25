"""Language discipline app REST API v1 urls."""

from rest_framework import routers

from .views.study import WordStudyViewSet

router = routers.DefaultRouter()

router.register(r'study', WordStudyViewSet, basename='study')
