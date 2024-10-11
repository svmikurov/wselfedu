"""Glossary app REST urls."""

from django.urls import path

from glossary.views.exercise import (
    glossary_exercise,
    glossary_exercise_parameters,
    update_term_study_progress,
)
from glossary.views.glossary import (
    GlossaryDetailAPIView,
    GlossaryListAPIView,
)

urlpatterns = [
    path(
        'api/v1/glossary/<int:pk>/',
        GlossaryDetailAPIView.as_view(),
        name='api_term',
    ),
    path(
        'api/v1/glossary/',
        GlossaryListAPIView.as_view(),
        name='api_glossary',
    ),
    path(
        'api/v1/glossary/progress/',
        update_term_study_progress,
        name='api_glossary_term_progress',
    ),
    path(
        'api/v1/glossary/exercise/',
        glossary_exercise,
        name='api_glossary_exercise',
    ),
    path(
        'api/v1/glossary/exercise/parameters/',
        glossary_exercise_parameters,
        name='api_glossary_exercise_parameters',
    ),
]
