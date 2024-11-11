"""Glossary app REST urls."""

from django.urls import path

from glossary.views.rest.exercise import (
    glossary_exercise,
    glossary_exercise_parameters,
    update_term_study_progress,
)
from glossary.views.rest.glossary import (
    CategoryTermListCreateAPIView,
    GlossaryCategoryDetailAPIView,
    GlossaryDetailAPIView,
    GlossaryListCreateAPIView,
)

# 'api/v1/glossary/
app_name = 'glossary_rest'

urlpatterns = [
    # Terms
    path('', GlossaryListCreateAPIView.as_view(), name='terms'),
    path('<int:pk>/', GlossaryDetailAPIView.as_view(), name='term'),
    path(
        'category/', CategoryTermListCreateAPIView.as_view(), name='category'
    ),  # noqa: E501
    path(
        'category/<int:pk>/',
        GlossaryCategoryDetailAPIView.as_view(),
        name='category',
    ),  # noqa: E501
    # Exercise
    path('progress/', update_term_study_progress, name='progress'),
    path('exercise/', glossary_exercise, name='exercise'),
    path('params/', glossary_exercise_parameters, name='params'),
]
