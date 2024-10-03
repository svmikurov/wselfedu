"""Task app urls module."""

from django.urls import path

from task import views

app_name = 'task'

urlpatterns = [
    path(
        'index/',
        views.IndexTaskView.as_view(),
        name='index',
    ),
    # --======= Math Tasks =======--
    path(
        'math-calculate-choice/',
        views.MathCalculateChoiceView.as_view(),
        name='math_calculate_choice',
    ),
    path(
        'math-calculate-demo/',
        views.MathCalculateDemoView.as_view(),
        name='math_calculate_demo',
    ),
    path(
        'math-calculate-solution/',
        views.MathCalculateSolutionView.as_view(),
        name='math_calculate_solution',
    ),
    path(
        'render-calculate-task/',
        views.render_task,
        name='render_calculate_task',
    ),
    # --=== Points Exercises ===--
    path(
        'math-set-table-mult-points/',
        views.SetMultiplicationTableExerciseView.as_view(),
        name='math_set_table_mult_points',
    ),
    # -- End Math Tasks --
    # --======= Foreign Tasks =======--
    path(
        'foreign-translate-choice/',
        views.ForeignWordTranslateChoiceView.as_view(),
        name='foreign_translate_choice',
    ),
    path(
        'foreign-translate-demo/',
        views.ForeignTranslateExerciseView.as_view(),
        name='foreign_translate_demo',
    ),
    path(
        'progress/<int:word_id>/',
        views.update_word_progress_view,
        name='progress',
    ),
    # -- End Foreign Tasks --
]
