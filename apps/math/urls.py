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
        TemplateView.as_view(
            template_name='math/exercise/calculation/index.html'
        ),
        name='math_exercises',
    ),
    # -------------------------------------------
    # Custom calculation exercises
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
    # Mentors's assigned calculation exercises
    # -------------------------------------------
    path(
        'exercise/calculation/mentor/',
        calculation.AssignedCalculationConditionMentorListView.as_view(),
        name='mentor_calculation_exercise_list',
    ),
    path(
        'exercise/calculation/mentor/create/',
        calculation.AssignedCalculationConditionMentorCreateView.as_view(),
        name='mentor_calculation_exercise_create',
    ),
    path(
        'exercise/calculation/mentor/<int:pk>/update/',
        calculation.AssignedCalculationConditionMentorUpdateView.as_view(),
        name='mentor_calculation_exercise_update',
    ),
    path(
        'exercise/calculation/mentor/<int:pk>/delete/',
        calculation.AssignedCalculationConditionMentorDeleteView.as_view(),
        name='mentor_calculation_exercise_delete',
    ),
    # -------------------------------------------
    # Student's assigned calculation exercises
    # -------------------------------------------
    path(
        'exercise/calculation/student/list/',
        calculation.StudentCalculationExerciseListVew.as_view(),
        name='student_calculation_exercise_list',
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
        calculation.CustomCalculationPerformView.as_view(),
        name='detail_calculation_exercise',
    ),
    path(  # exercise conditions assigned to the user
        'exercise/calculation/<int:pk>/student/',
        calculation.StudentCalculationPerformView.as_view(),
        name='student_calculation_exercise',
    ),
]
