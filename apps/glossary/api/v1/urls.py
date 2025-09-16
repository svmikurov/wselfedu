"""Glossary app API v1 urls."""

from rest_framework import routers

from .views import TermViewSet

router = routers.SimpleRouter()

router.register(r'terms', TermViewSet, basename='term')
