"""Foreign app REST urls."""

from django.urls import path

from foreign.views.rest import (
    WordDetailAPIView,
    WordListCreateAPIView,
    exercise_parameters,
)
from foreign.views.rest.exercise import translate_exercise

urlpatterns = [
    # Words.
    path(
        '',
        WordListCreateAPIView.as_view(),
        name='api-words',
    ),
    path(
        '<int:pk>/',
        WordDetailAPIView.as_view(),
        name='api-word',
    ),
    # Exercise.
    path(
        'params/',
        exercise_parameters,
    ),
    path(
        'exercise/',
        translate_exercise,
    ),
]
