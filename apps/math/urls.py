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
    # ===========================================
    # Exercise selection page
    # -------------------------------------------
    path(
        'exercises/',
        TemplateView.as_view(
            template_name='math/exercise/calculation/index.html'
        ),
        name='math_exercises',
    ),
    # ===========================================
    # Regular calculation exercises
    # -------------------------------------------
    path(
        'exercise/calculation/regular',
        calculation.ExerciseChoiceView.as_view(),
        name='select_regular_calculation',
    ),
    # ===========================================
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
    # ===========================================
    # Mentors's calculation exercises
    # -------------------------------------------
    # Assigned by the mentor for his students.
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
    path(
        'exercise/calculation/mentor/<int:pk>/perform/',
        calculation.MentorCalculationPerformView.as_view(),
        name='mentor_calculation_exercise_perform',
    ),
    # ===========================================
    # Student's calculation exercises
    # -------------------------------------------
    # Assigned to the student by his mentors.
    # -------------------------------------------
    path(
        'exercise/calculation/student/list/',
        calculation.StudentCalculationExerciseListVew.as_view(),
        name='student_calculation_exercise_list',
    ),
    # ===========================================
    # Calculation exercise performing
    # -------------------------------------------
    path(
        'exercise/calculation/performing/regular/',
        calculation.RegularPerformView.as_view(),
        name='regular_calculation_exercise',
    ),
    path(
        'exercise/calculation/performing/<int:pk>/custom/',
        calculation.CustomCalculationPerformView.as_view(),
        name='custom_calculation_exercise',
    ),
    path(
        'exercise/calculation/performing/<int:pk>/student/',
        calculation.StudentCalculationPerformView.as_view(),
        name='student_calculation_exercise',
    ),
]
