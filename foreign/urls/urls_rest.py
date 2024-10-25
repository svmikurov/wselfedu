"""Foreign app REST urls."""

from django.urls import path

from foreign.views.rest import (
    WordDetailAPIView,
    WordListCreateAPIView,
    exercise_parameters,
    translate_exercise,
    update_word_assessment_view,
)

app_name = 'foreign_rest'

urlpatterns = [
    # Words.
    path('', WordListCreateAPIView.as_view(), name='words'),
    path('<int:pk>/', WordDetailAPIView.as_view(), name='word'),
    # Exercise.
    path('params/', exercise_parameters, name='params'),
    path('exercise/', translate_exercise, name='exercise'),
    path('assessment/', update_word_assessment_view, name='assessment'),
]
