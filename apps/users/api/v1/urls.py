"""Defines Users application API urls."""

from rest_framework import routers

from apps.users.api.v1 import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'balance', views.BalanceViewSet, basename='balance')
