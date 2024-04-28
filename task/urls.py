from django.urls import path

from task import views

app_name = 'task'

urlpatterns = [
    path(
        'common-demo/',
        views.CommonTaskInterfaceView.as_view(),
        name='common_demo',
    ),
    path(
        'math-solutions/',
        views.MathSolutionsView.as_view(),
        name='math_solutions',
    ),
    path(
        'render-task/',
        views.render_task,
        name='render_task',
    ),
    # --======= Task word study =======--
    # Отображение параметров для выборки слов на задание.
    path(
        'words-choice/',
        views.WordChoiceView.as_view(),
        name='word_choice',
    ),
    # Создание задания и отображение с помощью ajax.
    path(
        'word-study-ajax/',
        views.WordStudyView.as_view(),
        name='word_study_ajax',
    ),
    # -- End Task word study --
]
