"""Defines authentication urls."""

from django.urls import path

from .views import SignUpView
from .views.account import AccountView

app_name = 'users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('<int:pk>/', AccountView.as_view(), name='account'),
]
