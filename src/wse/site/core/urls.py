"""URL configuration for settings project."""

from django.urls import path

from wse.site.core import views

urlpatterns = [
    path(
        'testing/',
        views.TestingExercisePerformView.as_view(),
        name='testing',
    ),
]
