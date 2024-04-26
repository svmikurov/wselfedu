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
        'select-calculations-task/',
        views.SelectMathTaskParamsView.as_view(),
        name='select_calculations_task',
    ),
]
