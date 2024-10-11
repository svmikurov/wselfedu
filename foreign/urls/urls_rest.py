"""Foreign app REST urls."""

from django.urls import path

from foreign.views.rest import (
    WordDetailAPIView,
    WordListCreateAPIView,
    exercise_parameters,
)

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
        'exercise/params/',
        exercise_parameters,
    ),
]
