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
]
