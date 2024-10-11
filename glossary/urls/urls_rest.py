"""Glossary app REST urls."""

from django.urls import path

from glossary.views.exercise import (
    glossary_exercise,
    glossary_exercise_parameters,
    update_term_study_progress,
)
from glossary.views.glossary import (
    GlossaryDetailAPIView,
    GlossaryListCreateAPIView,
)

urlpatterns = [
    path(
        '',
        GlossaryListCreateAPIView.as_view(),
        name='api_glossary',
    ),
    path(
        '<int:pk>/',
        GlossaryDetailAPIView.as_view(),
        name='api_term',
    ),
    path(
        'progress/',
        update_term_study_progress,
        name='api_glossary_term_progress',
    ),
    path(
        'exercise/',
        glossary_exercise,
        name='api_glossary_exercise',
    ),
    path(
        'params/',
        glossary_exercise_parameters,
        name='api_glossary_exercise_parameters',
    ),
]
