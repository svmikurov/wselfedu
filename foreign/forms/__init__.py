"""Foreign words forms package."""

from foreign.forms.category import CategoryForm
from foreign.forms.source import SourceForm
from foreign.forms.word import WordForm
from foreign.forms.word_choice import ForeignTranslateChoiceForm

__all__ = [
    'CategoryForm',
    'ForeignTranslateChoiceForm',
    'SourceForm',
    'WordForm',
]
