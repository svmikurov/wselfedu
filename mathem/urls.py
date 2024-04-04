from django.urls import path

from mathem import views

app_name = 'mathem'

urlpatterns = [
    path(
        '',
        views.HomeView.as_view(),
        name='home',
    ),
    path(
        'mult/',
        views.MultTaskView.as_view(),
        name='mult',
    ),
    path(
        'calculations/',
        views.CalculationsView.as_view(),
        name='calculations',
    ),
    path(
        'task_ajax/',
        views.TaskAjax.as_view(),
        name='task_ajax',
    ),
    # Math task choice
    path(
        'math-task-choice/',
        views.MathTaskChoiceView.as_view(),
        name='math_task_choice',
    ),
    # Math calculations using ajax
    path(
        'math-task-calculations/',
        views.MathTaskCalculationsView.as_view(),
        name='math_task_calculations',
    ),
]
