"""URL configuration for settings project."""

from django.urls import path

from wse.site.core import views

urlpatterns = [
    path('exercise/', views.ExercisePerformView.as_view(), name='exercise'),
]
