"""Glossary app DRF urls."""

from django.urls import path
from django.views.generic import TemplateView

app_name = 'glossary'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='glossary/home.html'),
        name='home',
    ),
    path(
        '',
        TemplateView.as_view(template_name='glossary/list.html'),
        name='list',
    ),
    path(
        '',
        TemplateView.as_view(template_name='glossary/params.html'),
        name='params',
    ),
]
