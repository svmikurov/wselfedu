from django.urls import path

from mathem import views
from mathem.views.calculations_view import TaskAjax

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
        TaskAjax.as_view(),
        name='task_ajax',
    )
]
