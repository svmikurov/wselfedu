"""Defines Core app web urls."""

from django.urls import path
from django.views.generic import TemplateView

from .views import source

app_name = 'core'

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # -------------------------------------------
    # Source
    # -------------------------------------------
    path(
        'source/',
        source.SourceListView.as_view(),
        name='source_list',
    ),
    path(
        'source/create/',
        source.SourceCreateView.as_view(),
        name='source_create',
    ),
    path(
        'source/<int:pk>/update/',
        source.SourceUpdateView.as_view(),
        name='source_update',
    ),
    path(
        'source/<int:pk>/delete/',
        source.SourceDeleteView.as_view(),
        name='source_delete',
    ),
]
