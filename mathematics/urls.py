"""Mathematics application urlpatterns."""

from django.urls import path
from django.views.generic import TemplateView

from mathematics.views import (
    MathCalculateChoiceView,
    MathCalculateDemoView,
    MathCalculateSolutionView,
    SetMultiplicationTableExerciseView,
    render_task,
)

app_name = 'math'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='mathematics/main.html'),
        name='main',
    ),
    path(
        'math-calculate-choice/',
        MathCalculateChoiceView.as_view(),
        name='math_calculate_choice',
    ),
    path(
        'math-calculate-demo/',
        MathCalculateDemoView.as_view(),
        name='math_calculate_demo',
    ),
    path(
        'math-calculate-solution/',
        MathCalculateSolutionView.as_view(),
        name='math_calculate_solution',
    ),
    path(
        'render-calculate-task/',
        render_task,
        name='render_calculate_task',
    ),
    # Points Exercises
    path(
        'math-set-table-mult-points/',
        SetMultiplicationTableExerciseView.as_view(),
        name='math_set_table_mult_points',
    ),
]
