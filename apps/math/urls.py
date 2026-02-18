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
    # Calculation exercise selection
    # Contains:
    #   - form for the exercise conditions
    # -------------------------------------------
    path(
        'exercise/calculation/',
        calculation.ExerciseChoiceView.as_view(),
        name='select_regular_calculation',
    ),
    # -------------------------------------------
    # Calculation exercise performing
    # -------------------------------------------
    # Contains:
    #   - form for the exercise performing the
    #     current selected exercise conditions
    path(
        'exercise/calculation/regular/performing/',
        calculation.RegularPerformView.as_view(),
        name='regular_calculation_exercise',
    ),
    path(  # exercise conditions saved by the user
        'exercise/calculation/<int:pk>/detail/',
        calculation.DetailPerformView.as_view(),
        name='detail_calculation_exercise',
    ),
    path(  # exercise conditions assigned to the user
        'exercise/calculation/<int:pk>/assigned/',
        calculation.AssignedPerformView.as_view(),
        name='assigned_calculation_exercise',
    ),
    # -------------------------------------------
    # Custom calculation exercise CRUD
    # -------------------------------------------
    path(
        'exercise/calculation/regular/',
        calculation.CalculationListView.as_view(),
        name='regular_calculation_exercise_list',
    ),
    path(
        'exercise/calculation/regular/create/',
        calculation.CalculationCreateView.as_view(),
        name='regular_calculation_exercise_create',
    ),
    path(
        'exercise/calculation/regular/<int:pk>/update/',
        calculation.CalculationUpdateView.as_view(),
        name='regular_calculation_exercise_update',
    ),
    path(
        'exercise/calculation/regular/<int:pk>/delete/',
        calculation.CalculationDeleteView.as_view(),
        name='regular_calculation_exercise_delete',
    ),
    # -------------------------------------------
    # Calculation exercise CRUD for mentor
    # -------------------------------------------
    path(
        'exercise/calculation/mentor/list/',
        calculation.AssignedCalculationConditionMentorListView.as_view(),
        name='mentor_calculation_exercise_list',
    ),
    path(
        'exercise/calculation/mentor/create/',
        calculation.AssignedCalculationConditionMentorCreateView.as_view(),
        name='mentor_calculation_exercise_create',
    ),
    path(
        'exercise/calculation/mentor/<int:pk>/delete/',
        calculation.AssignedCalculationConditionMentorDeleteView.as_view(),
        name='mentor_calculation_exercise_delete',
    ),
]
