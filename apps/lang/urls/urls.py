"""Language discipline web urls paths."""

from django.urls import path
from django.views.generic import TemplateView

from .. import views
from ..views import rule
from ..views.exercise import assignments, mentorship, student

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='lang/index.html'),
        name='index',
    ),
    # -----------------~~~~~~~~~~~~~~~~
    # English language study curriculum
    # -----------------~~~~~~~~~~~~~~~~
    path(
        'tasks/',
        student.ExercisesForTodayView.as_view(),
        name='english_tasks',
    ),
    path(
        'assign/',
        assignments.AssignedTranslationView.as_view(),
        name='english_assign_exercises',
    ),
    # Exercise assignation
    path(
        'english/mentor/exercise/<int:pk>/assignation/',
        mentorship.MentorExerciseUpdateView.as_view(),
        name='english_mentor_exercise_assign',
    ),
    path(
        'english/mentor/exercise/assignation/create/',
        assignments.ExerciseAssignationCreateView.as_view(),
        name='english_mentor_exercise_assignation_create',
    ),
    path(
        'english/mentor/exercise/assigned/',
        assignments.ExerciseAssignationListView.as_view(),
        name='english_mentor_exercises_assignation_list',
    ),
    path(
        'english/mentor/exercise/assigned/<int:pk>/delete/',
        assignments.EnglishAssignedExerciseDeleteView.as_view(),
        name='english_mentor_exercises_assignation_delete',
    ),
    # -----------------~~~~~~~~~~~~~~~~
    # English language study mentorship
    # -----------------~~~~~~~~~~~~~~~~
    path(
        'rule/<int:pk>/assignment/create/',
        views.RuleAssignmentCreate.as_view(),
        name='english_rule_assignment_create',
    ),
    # ----------------------
    # English language rules
    # ----------------------
    path(
        'rule/',
        views.RuleView.as_view(),
        name='english_rule',
    ),
    path(
        'rule/list/',
        views.RuleListView.as_view(),
        name='english_rule_list',
    ),
    path(
        'rule/create/',
        views.RuleCreateView.as_view(),
        name='english_rule_create',
    ),
    path(
        'rule/<int:pk>/detail/',
        views.RuleDetailView.as_view(),
        name='english_rule_detail',
    ),
    path(
        'rule/<int:pk>/update/',
        views.RuleUpdateView.as_view(),
        name='english_rule_update',
    ),
    path(
        'rule/<int:pk>/delete/',
        views.RuleDeleteView.as_view(),
        name='english_rule_delete',
    ),
    # Rule clause example & exception edit
    path(
        'rule/<int:pk>/clause/create/',
        views.ClauseCreateView.as_view(),
        name='english_clause_create',
    ),
    path(
        'rule/<int:pk>/clause/update/',
        views.ClauseUpdateView.as_view(),
        name='english_clause_update',
    ),
    path(  # Add word example
        'rule/<int:pk>/add-word-example/',
        views.WordExampleAddView.as_view(),
        name='english_example_word_add',
    ),
    path(  # List of word example
        'rule/<int:pk>/word-example-list/',
        views.WordExampleListView.as_view(),
        name='english_example_word_list',
    ),
    path(  # Delete the word example
        'rule/<int:pk>/delete-word-example/',
        rule.WordExampleDeleteView.as_view(),
        name='english_example_word_delete',
    ),
    path(  # Add task example
        'rule/<int:pk>/add-task-example/',
        views.TaskExampleAddView.as_view(),
        name='english_example_task_add',
    ),
    path(  # List of task example
        'rule/<int:pk>/task-example-list/',
        rule.TaskExampleListView.as_view(),
        name='english_example_task_list',
    ),
    path(  # Delete the task example
        'rule/<int:pk>/delete-task-example/',
        rule.TaskExampleDeleteView.as_view(),
        name='english_example_task_delete',
    ),
    path(
        'rule/<int:pk>/add-exception/',
        views.ExceptionAddView.as_view(),
        name='english_exception_add',
    ),
    # --------------
    # Study settings
    # --------------
    path(
        'settings/',
        views.study_settings_view,
        name='settings',
    ),
    #
    # ==================== Refactored ====================
    #
    # -------------------------
    # Mentor-assigned exercises
    # -------------------------
    path(
        'english/mentor/exercises/',
        mentorship.MentorExerciseIndexView.as_view(),
        name='english_mentor_exercises',
    ),
    path(
        'english/mentor/exercises/list/',
        mentorship.MentorExerciseListView.as_view(),
        name='english_mentor_exercises_list',
    ),
    path(
        'english/mentor/exercises/create/',
        mentorship.MentorExerciseCreateView.as_view(),
        name='english_mentor_exercise_create',
    ),
    path(
        'english/mentor/exercise/<int:pk>/update/',
        mentorship.MentorExerciseUpdateView.as_view(),
        name='english_mentor_exercise_update',
    ),
    path(
        'english/mentor/exercise/<int:pk>/delete/',
        mentorship.MentorExerciseDeleteView.as_view(),
        name='english_mentor_exercise_delete',
    ),
]
