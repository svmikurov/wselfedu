"""Defines math app api v1 url paths."""

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(
    '',
    views.IndexViewSet,
    basename='math_index',
)
router.register(
    'exercise',
    views.CalculationViewSet,
    basename='calculation',
)
router.register(
    r'assigned/(?P<assignation_id>\d+)',
    views.ExerciseViewSet,
    basename='assigned_exercise',
)
