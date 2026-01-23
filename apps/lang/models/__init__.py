"""Language discipline models."""

__all__ = [
    # Translation
    'NativeWord',
    'EnglishWord',
    'EnglishTranslation',
    # Exercise
    'Exercise',
    'EnglishAssignedExercise',
    'EnglishTranslationExercise',
    # Parameters
    'Parameters',
    'TranslationSetting',
    'PresentationSettings',
    # Rule
    'Rule',
    'RuleClause',
    'RuleException',
    'ExampleType',
    'RuleExample',
    'RuleTaskExample',
    'MentorshipEnglishRule',
    # Meta
    'Mark',
    'TranslationMark',
    'Category',
]

from .assignment.mentorship.rule import (
    MentorshipEnglishRule,
)
from .category import Category
from .exercise import (
    EnglishAssignedExercise,
    EnglishTranslationExercise,
)
from .exercise.exercise import Exercise
from .exercise.parameters import (
    Parameters,
    PresentationSettings,
    TranslationSetting,
)
from .mark import Mark, TranslationMark
from .rule import (
    ExampleType,
    Rule,
    RuleClause,
    RuleExample,
    RuleException,
    RuleTaskExample,
)
from .translation import EnglishTranslation
from .word import EnglishWord, NativeWord
