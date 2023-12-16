from django.urls import path

from . import views

app_name = 'math'

urlpatterns = [
    path(
        '',
        views.HomeView.as_view(template_name='mathem/home.html'),
        name='home',
    ),
    path(
        'mult/',
        views.MultTaskView.as_view(),
        name='mult',
    ),
]
