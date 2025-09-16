"""Glossary app urls."""

from django.urls import path

from apps.glossary.views import IndexGlossaryView
from apps.glossary.views.term import (
    TermCreateView,
    TermDeleteView,
    TermDetailView,
    TermListView,
    TermUpdateView,
)

app_name = 'glossary'

urlpatterns = [
    path('', IndexGlossaryView.as_view(), name='index'),
    # Path 'term/' reserved for chapter definition
    path(
        'term/create/',
        TermCreateView.as_view(),
        name='term_create',
    ),
    path(
        'term/<int:pk>/',
        TermDetailView.as_view(),
        name='term_detail',
    ),
    path(
        'term/<int:pk>/update/',
        TermUpdateView.as_view(),
        name='term_update',
    ),
    path(
        'term/list/',
        TermListView.as_view(),
        name='term_list',
    ),
    path(
        'term/<int:pk>/delete/',
        TermDeleteView.as_view(),
        name='term_delete',
    ),
    path(
        'term/study/',
        IndexGlossaryView.as_view(),
        name='term_study',
    ),
]
