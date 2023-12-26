from django.urls import path

from . import views

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
]
