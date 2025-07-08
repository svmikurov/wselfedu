"""Defines Mathematical application urls."""

from django.urls import path
from django.views.generic import TemplateView

app_name = 'math'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='math/index.html'),
        name='index',
    ),
]
