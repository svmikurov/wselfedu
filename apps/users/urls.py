"""Defines Users app web paths."""

from django.urls import path

from .views import ProfileView

urlpatterns = [
    path('<int:pk>/profile/', ProfileView.as_view(), name='profile'),
]
