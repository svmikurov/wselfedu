from django.urls import path

from task import views

app_name = 'task'

urlpatterns = [
    # --======= Math Tasks =======--
    path(
        'math-calculate-choice/',
        views.MathCalculationChoiceView.as_view(),
        name='math_calculate_choice',
    ),
    path(
        'math-calculate-demo/',
        views.MathCalculationDemoView.as_view(),
        name='math_calculate_demo',
    ),
    path(
        'math-calculate-solution/',
        views.MathCalculationSolutionView.as_view(),
        name='math_calculate_solution',
    ),
    path(
        'render-calculate-task/',
        views.render_task,
        name='render_calculate_task',
    ),  # -- End Math Tasks --
    #
    # --======= English Tasks =======--
    path(
        'english-translate-choice/',
        views.EnglishTranslateChoiceView.as_view(),
        name='english_translate_choice',
    ),
    path(
        'english-translate-demo/',
        views.EnglishTranslateDemoView.as_view(),
        name='english_translate_demo',
    ),  # -- End English Tasks --
]
