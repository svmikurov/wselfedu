"""Mathematical discipline web url paths."""

from django.urls import path
from django.views.generic import TemplateView

from .views.exercise import calculation

app_name = 'math'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='math/index.html'),
        name='index',
    ),
    path(
        '',
        calculation.CalculationView.as_view(),
        name='exercise_calculation',
    ),
]
