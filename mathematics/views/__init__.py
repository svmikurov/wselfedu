"""Mathematics app views."""

from mathematics.views.calculation import (
    MathCalculateChoiceView,
    MathCalculateDemoView,
    MathCalculateSolutionView,
    SetMultiplicationTableExerciseView,
    render_task,
)

__all__ = (
    'MathCalculateChoiceView',
    'MathCalculateDemoView',
    'MathCalculateSolutionView',
    'render_task',
    'SetMultiplicationTableExerciseView',
)
