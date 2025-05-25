"""Defines Mathematical app REST API urls."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'calculation', views.ExerciseViewSet, basename='calculation')

urlpatterns = [
    path('', include(router.urls)),
]
