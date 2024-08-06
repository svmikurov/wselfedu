"""Task app views module."""

from task.views.english_translate_views import (
    EnglishTranslateChoiceView,
    EnglishTranslateExerciseView,
    update_words_knowledge_assessment_view,
)
from task.views.index import IndexTaskView
from task.views.math_calculate_views import (
    MathCalculateChoiceView,
    MathCalculateDemoView,
    MathCalculateSolutionView,
    render_task,
)
from task.views.set_points_tasks import SetMultiplicationTableExerciseView

__all__ = [
    'MathCalculateChoiceView',
    'MathCalculateDemoView',
    'MathCalculateSolutionView',
    'render_task',
    'EnglishTranslateChoiceView',
    'EnglishTranslateExerciseView',
    'update_words_knowledge_assessment_view',
    'IndexTaskView',
    'SetMultiplicationTableExerciseView',
]
