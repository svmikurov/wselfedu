"""Defines Core app api v1 url paths."""

from rest_framework import routers

from .views.index import IndexViewSet

router = routers.DefaultRouter()
router.register(r'', IndexViewSet, basename='core_index')
