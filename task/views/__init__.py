"""Task app views."""

from glossary.views_drf import update_term_study_progress
from task.views.foreign_exercise_views import (
    ForeignTranslateExerciseView,
    ForeignWordTranslateChoiceView,
    update_word_progress_view,
)
from task.views.glossary_exercise_drf_views import (
    glossary_exercise,
    glossary_exercise_parameters,
)
from task.views.index import IndexTaskView
from task.views.math_calculate_views import (
    MathCalculateChoiceView,
    MathCalculateDemoView,
    MathCalculateSolutionView,
    SetMultiplicationTableExerciseView,
    render_task,
)

__all__ = [
    # Task Index
    'IndexTaskView',
    # Foreign
    'ForeignWordTranslateChoiceView',
    'ForeignTranslateExerciseView',
    'update_word_progress_view',
    # Glossary
    'update_term_study_progress',
    'glossary_exercise',
    'glossary_exercise_parameters',
    # Mathematical
    'MathCalculateChoiceView',
    'MathCalculateDemoView',
    'MathCalculateSolutionView',
    'render_task',
    'SetMultiplicationTableExerciseView',
]
