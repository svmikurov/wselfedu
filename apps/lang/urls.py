"""Language discipline web urls paths."""

from django.urls import path

from . import views
from .views import category, mark, rule, translation
from .views.exercise import assignments, curriculum

app_name = 'lang'

urlpatterns = [
    path('', views.IndexLangView.as_view(), name='index'),
    # -----------------~~~~~~~~~~~~~~~~
    # English language study curriculum
    # -----------------~~~~~~~~~~~~~~~~
    path(
        'tasks/',
        curriculum.ExercisesForTodayView.as_view(),
        name='english_tasks',
    ),
    path(
        'assign/',
        assignments.AssignedTranslationView.as_view(),
        name='english_assign_exercises',
    ),
    path(
        'english/mentor/exercises/',
        assignments.MentorExercisesIndexView.as_view(),
        name='english_mentor_exercises',
    ),
    path(
        'english/mentor/exercises/management/',
        assignments.MentorExerciseListView.as_view(),
        name='english_mentor_exercises_management',
    ),
    path(
        'english/mentor/exercises/create/',
        assignments.MentorExerciseCreateView.as_view(),
        name='english_mentor_exercise_create',
    ),
    # Exercise update, delete
    path(
        'english/mentor/exercise/<int:pk>/update/',
        assignments.MentorExerciseUpdateView.as_view(),
        name='english_mentor_exercise_update',
    ),
    path(
        'english/mentor/exercise/<int:pk>/delete/',
        assignments.MentorExerciseDeleteView.as_view(),
        name='english_mentor_exercise_delete',
    ),
    # Exercise assignation
    path(
        'english/mentor/exercise/<int:pk>/assignation/',
        assignments.MentorExerciseUpdateView.as_view(),
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
    # -----------------
    # Translation study
    # -----------------
    # - Presentation
    path(
        'translation/english/study/',
        views.EnglishTranslationStudyView.as_view(),
        name='translation_english_study',
    ),
    path(
        'translation/english/study/case/',
        views.EnglishTranslationStudyCaseView.as_view(),
        name='translation_english_study_case',
    ),
    # - Test
    path(
        'translation/english/test/',
        views.TranslationTestView.as_view(),
        name='translation_english_test',
    ),
    path(
        'translation/english/test/progress/',
        views.TranslationTestProgressView.as_view(),
        name='translation_english_test_progress',
    ),
    path(
        'translation/english/test/mentorship/',
        views.TranslationTestMentorshipView.as_view(),
        name='translation_english_test_mentorship',
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
    # -----------
    # Translation
    # -----------
    path(
        'english/translation/',
        translation.EnglishTranslationIndexView.as_view(),
        name='english_translation_index',
    ),
    path(
        'english/translation/list/',
        translation.EnglishTranslationListView.as_view(),
        name='english_translation_list',
    ),
    path(
        'english/translation/create/',
        translation.EnglishTranslationCreateView.as_view(),
        name='english_translation_create',
    ),
    path(
        'english/translation/<int:pk>/update/',
        translation.EnglishTranslationUpdateView.as_view(),
        name='english_translation_update',
    ),
    path(
        'english/translation/<int:pk>/delete/',
        translation.EnglishTranslationDeleteView.as_view(),
        name='english_translation_delete',
    ),
    # ----
    # Mark
    # ----
    path(
        'mark/list/',
        mark.MarkListView.as_view(),
        name='mark_list',
    ),
    path(
        'mark/create/',
        mark.MarkCreateView.as_view(),
        name='mark_create',
    ),
    path(
        'mark/<int:pk>/update/',
        mark.MarkUpdateView.as_view(),
        name='mark_update',
    ),
    path(
        'mark/<int:pk>/delete/',
        mark.MarkDeleteView.as_view(),
        name='mark_delete',
    ),
    # --------
    # Category
    # --------
    path(
        'category/list/',
        category.CategoryListView.as_view(),
        name='category_list',
    ),
    path(
        'category/create/',
        category.CategoryCreateView.as_view(),
        name='category_create',
    ),
    path(
        'category/<int:pk>/update/',
        category.CategoryUpdateView.as_view(),
        name='category_update',
    ),
    path(
        'category/<int:pk>/delete/',
        category.CategoryDeleteView.as_view(),
        name='category_delete',
    ),
]
