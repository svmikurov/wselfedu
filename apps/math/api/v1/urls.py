"""Defines math app api v1 url paths."""

from rest_framework import routers

from .views import IndexViewSet

router = routers.DefaultRouter()
router.register('', IndexViewSet, basename='math_index')
