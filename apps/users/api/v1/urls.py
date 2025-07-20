"""Defines users app api v1 url paths."""

from rest_framework import routers

from .views.balance import BalanceViewSet

router = routers.DefaultRouter()
router.register(r'balance', BalanceViewSet, 'balance')
