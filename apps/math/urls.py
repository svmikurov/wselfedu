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
        'exercises/',
        TemplateView.as_view(template_name='math/exercise/index.html'),
        name='math_exercises',
    ),
    path(
        'exercise/calculation/',
        calculation.RegularCalculationView.as_view(),
        name='regular_calculation_exercise',
    ),
    path(
        'exercise/calculation/<int:pk>/',
        calculation.DetailCalculationView.as_view(),
        name='detail_calculation_exercise',
    ),
]
