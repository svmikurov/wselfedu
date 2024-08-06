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
    #
    # -- End Math Tasks --
    #
    # --======= English Tasks =======--
    path(
        'english-translate-choice/',
        views.EnglishTranslateChoiceView.as_view(),
        name='english_translate_choice',
    ),
    path(
        'english-translate-demo/',
        views.EnglishTranslateExerciseView.as_view(),
        name='english_translate_demo',
    ),
    path(
        'knowledge-assessment/<int:word_id>/',
        views.update_words_knowledge_assessment_view,
        name='knowledge_assessment',
    ),
    # -- End English Tasks --
]
