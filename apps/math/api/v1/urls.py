"""Defines Mathematical application API urls."""

from rest_framework import routers

from apps.math.api.v1 import views

router = routers.DefaultRouter()
router.register(r'index', views.MathIndexViewSet, basename='index')
router.register(r'exercise', views.SimpleCalcViewSet, basename='exercise')
