"""Term app REST urls."""

from django.urls import path

from glossary.views.rest.exercise import (
    glossary_exercise_view,
    glossary_favorites_view,
    glossary_params_view,
    update_term_study_progress,
)
from glossary.views.rest.term import (
    CategoryTermDetailAPIView,
    CategoryTermListCreateAPIView,
    TermDetailAPIView,
    TermListCreateAPIView,
)

# 'api/v1/glossary/
app_name = 'glossary_rest'


urlpatterns = [
    # Terms
    path('', TermListCreateAPIView.as_view(), name='terms'),
    path('<int:pk>/', TermDetailAPIView.as_view(), name='term'),
    path(
        'category/', CategoryTermListCreateAPIView.as_view(), name='category'
    ),  # noqa: E501
    path(
        'category/<int:pk>/',
        CategoryTermDetailAPIView.as_view(),
        name='category',
    ),  # noqa: E501
    # Exercise
    path('progress/', update_term_study_progress, name='progress'),
    path('exercise/', glossary_exercise_view, name='exercise'),
    path('favorites/', glossary_favorites_view, name='favorites'),
    path('params/', glossary_params_view, name='params'),
]
