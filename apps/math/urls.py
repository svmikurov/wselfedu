"""Mathematical discipline web url paths."""

from django.urls import path
from django.views.generic import TemplateView

from .views.exercise import calculation

app_name = 'math'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='math/index.html'),
        name='index',
    ),
    # -------------------------------------------
    # Exercise selection page
    # -------------------------------------------
    path(
        'exercises/',
        TemplateView.as_view(template_name='math/exercise/index.html'),
        name='math_exercises',
    ),
    # -------------------------------------------
    # Calculation exercise selection page
    # Contains:
    #   - form for the exercise conditions
    #   - table of exercises saved by the user
    #   - table of exercises assigned to the user
    # -------------------------------------------
    path(
        'exercise/calculation/',
        calculation.CalculationConditionsView.as_view(),
        name='select_regular_calculation',
    ),
    # -------------------------------------------
    # Calculation exercise performing pages
    # -------------------------------------------
    path(  # current selected exercise conditions
        'exercise/calculation/regular/',
        calculation.RegularCalculationView.as_view(),
        name='regular_calculation_exercise',
    ),
    path(  # exercise conditions saved by the user
        'exercise/calculation/<int:pk>/detail/',
        calculation.DetailCalculationView.as_view(),
        name='detail_calculation_exercise',
    ),
    path(  # exercise conditions assigned to the user
        'exercise/calculation/<int:pk>/assigned/',
        calculation.DetailCalculationView.as_view(),
        name='assigned_calculation_exercise',
    ),
]
