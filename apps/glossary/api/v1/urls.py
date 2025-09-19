"""Glossary app API v1 urls."""

from rest_framework import routers

from apps.glossary.api.v1.views.study import TermsStudyViewSet

from .views import TermViewSet

router = routers.SimpleRouter()

router.register(r'terms', TermViewSet, basename='term')
router.register(r'study', TermsStudyViewSet, basename='study')
