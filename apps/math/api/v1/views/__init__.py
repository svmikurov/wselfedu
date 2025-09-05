"""Contains Math app API views."""

__all__ = [
    'CalculationViewSet',
    'ExerciseViewSet',
    'IndexViewSet',
]

from .assigned import ExerciseViewSet
from .calculation import CalculationViewSet
from .index import IndexViewSet
