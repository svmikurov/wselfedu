"""User application rest urls."""

from django.urls import path

from users.views.rest.views import render_user_data

urlpatterns = [
    path(
        'data/',
        render_user_data,
        name='data',
    ),
]
