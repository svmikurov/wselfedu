"""Contains mathematical application models."""

__all__ = [
    'MathTaskChoice',
    'SimplCalcReward',
    'SimpleTask',
]

from apps.math.models.points import SimplCalcReward
from apps.math.models.simple import MathTaskChoice, SimpleTask
