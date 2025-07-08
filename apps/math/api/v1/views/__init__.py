"""Contains math app views."""

__all__ = [
    'MathIndexViewSet',
    'SimpleCalcViewSet',
]

from apps.math.api.v1.views.index import MathIndexViewSet
from apps.math.api.v1.views.simple_calc import SimpleCalcViewSet
