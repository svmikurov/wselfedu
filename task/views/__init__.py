"""Task app views."""

from task.views.english_translate_views import (
    EnglishTranslateChoiceView,
    EnglishTranslateExerciseView,
    update_words_knowledge_assessment_view,
)
from task.views.exercise_glossary_views import (
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
    # English
    'EnglishTranslateChoiceView',
    'EnglishTranslateExerciseView',
    'update_words_knowledge_assessment_view',
    # Glossary
    'glossary_exercise',
    'glossary_exercise_parameters',
    # Mathematical
    'MathCalculateChoiceView',
    'MathCalculateDemoView',
    'MathCalculateSolutionView',
    'render_task',
    'SetMultiplicationTableExerciseView',
]
