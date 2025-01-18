"""Glossary app REST urls."""

from django.urls import path

from glossary.views.rest import (
    glossary_exercise_view,
    glossary_params_view,
    update_term_favorites_view,
    update_term_progress_view,
    glossary_selected_view,
    TermDetailAPIView,
    TermListCreateAPIView,
)

app_name = 'glossary_rest'

urlpatterns = [
    # Terms
    path('', TermListCreateAPIView.as_view(), name='terms'),
    path('<int:pk>/', TermDetailAPIView.as_view(), name='term'),
    # Exercise
    path('params/', glossary_params_view, name='params'),
    path('selected/', glossary_selected_view, name='selected'),
    path('exercise/', glossary_exercise_view, name='exercise'),
    path('favorites/', update_term_favorites_view, name='favorites'),
    path('progress/', update_term_progress_view, name='progress'),
]
