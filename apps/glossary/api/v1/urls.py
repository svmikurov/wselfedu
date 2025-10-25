"""Glossary discipline app REST API v1 urls."""

from rest_framework import routers

from .views import TermStudyViewSet, TermViewSet

router = routers.DefaultRouter()

router.register(r'terms', TermViewSet, basename='term')
router.register(r'study', TermStudyViewSet, basename='study')
