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

from .views import assertion

app_name = 'glossary'

urlpatterns = [
    path('', IndexGlossaryView.as_view(), name='index'),
    path(
        'term/',
        TermListView.as_view(),
        name='term_list',
    ),
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
        'term/<int:pk>/delete/',
        TermDeleteView.as_view(),
        name='term_delete',
    ),
    path(
        'term/study/',
        IndexGlossaryView.as_view(),
        name='term_study',
    ),
    path(
        'term/assertion/create/',
        assertion.AssertionCreateView.as_view(),
        name='assertion_create',
    ),
]
