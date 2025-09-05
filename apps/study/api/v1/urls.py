"""Defines Core app api v1 url paths."""

from rest_framework import routers

from . import views

app_name = 'core'

router = routers.DefaultRouter()
router.register(
    r'assigned',
    views.AssignedExercisesViewSet,
    basename='assigned_mentor',
)
