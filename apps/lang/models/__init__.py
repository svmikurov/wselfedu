"""Language discipline models."""

__all__ = [
    # Translation
    'NativeWord',
    'EnglishWord',
    'EnglishTranslation',
    # Exercise
    'LanguageExercise',
    'EnglishAssignedExercise',
    'EnglishTranslationExercise',
    # Parameters
    'ExerciseConditions',
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
    # Progress
    'EnglishTranslationStudyProgress',
    # Meta
    'Mark',
    'TranslationMark',
    'Category',
]

from .assignment.mentorship.exercise import EnglishAssignedExercise
from .assignment.mentorship.rule import MentorshipEnglishRule
from .category import Category
from .exercise.name import LanguageExercise
from .exercise.params.lookup_conditions import ExerciseConditions
from .exercise.params.presentation_config import PresentationSettings
from .exercise.params.translation_settings import TranslationSetting
from .exercise.translation.exercise import (
    EnglishTranslationExercise,
    EnglishTranslationStudyProgress,
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
from .translation.english import EnglishTranslation
from .translation.word import EnglishWord, NativeWord
