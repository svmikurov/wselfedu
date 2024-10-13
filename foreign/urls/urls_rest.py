"""Foreign app REST urls."""

from django.urls import path

from foreign.views.rest import (
    WordDetailAPIView,
    WordListCreateAPIView,
    exercise_parameters,
)
from foreign.views.rest.exercise import translate_exercise

app_name = 'rest_foreign'

urlpatterns = [
    # Words.
    path('', WordListCreateAPIView.as_view(), name='words'),
    path('<int:pk>/', WordDetailAPIView.as_view(), name='word'),
    # Exercise.
    path('params/', exercise_parameters, name='params'),
    path('exercise/', translate_exercise, name='exercise'),
]
