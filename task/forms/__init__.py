"""Task app forms module."""

from task.forms.english_translate_choice_form import (
    EnglishTranslateChoiceForm,
)
from task.forms.math_calculate_choice_form import MathCalculationChoiceForm
from task.forms.user_input_form import NumberInputForm

__all__ = [
    'MathCalculationChoiceForm',
    'NumberInputForm',
    'EnglishTranslateChoiceForm',
]
