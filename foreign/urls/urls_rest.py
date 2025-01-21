"""Foreign app REST urls."""

from django.urls import path

from foreign.views.rest import (
    WordDetailAPIView,
    WordListCreateAPIView,
    foreign_exercise_view,
    foreign_params_view,
    foreign_selected_view,
    update_word_favorites_view,
    update_word_progress_view,
)

app_name = 'foreign_rest'

urlpatterns = [
    # Words
    path('', WordListCreateAPIView.as_view(), name='words'),
    path('<int:pk>/', WordDetailAPIView.as_view(), name='word'),
    # Exercise
    path('params/', foreign_params_view, name='params'),
    path('selected/', foreign_selected_view, name='selected'),
    path('exercise/', foreign_exercise_view, name='exercise'),
    path('favorites/', update_word_favorites_view, name='favorites'),
    path('progress/', update_word_progress_view, name='progress'),
]
