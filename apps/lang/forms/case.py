"""Study case parameters form."""

from typing import Any, List

from django import forms

from .. import models


class IntegerListField(forms.Field):
    """Field for a list of integers from QueryDict."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Initialize with MultipleHiddenInput widget."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
        self.widget = forms.MultipleHiddenInput()

    def bound_data(
        self,
        data: object,
        initial: object,
    ) -> List[str] | Any:  # noqa: ANN401
        """Get list values from QueryDict using getlist() method."""
        if hasattr(data, 'getlist'):
            return data.getlist(self.name, [])  # type: ignore[attr-defined]
        return super().bound_data(data, initial)

    def to_python(self, value: object) -> List[int]:
        """Convert input to list of integers."""
        if not value:
            return []

        # Normalize input to list
        if isinstance(value, str):
            items = [value]
        elif isinstance(value, list):
            items = value
        else:
            items = [str(value)]

        # Convert valid items to integers
        result: List[int] = []
        for item in items:
            if item and item != 'None' and item != '':
                try:
                    result.append(int(item))
                except (ValueError, TypeError):
                    continue

        return result


class CaseRequestForm(forms.Form):
    """Case parameters request form.

    Validates and converts to python dict the request data.
    """

    # Translation parameters
    category = forms.IntegerField(required=False)
    source = forms.IntegerField(required=False)
    mark = IntegerListField(required=False)
    start_period = forms.IntegerField(required=False)
    end_period = forms.IntegerField(required=False)

    # - progress phases
    is_study = forms.BooleanField(required=False)
    is_repeat = forms.BooleanField(required=False)
    is_examine = forms.BooleanField(required=False)
    is_know = forms.BooleanField(required=False)

    # Translation settings
    translation_order = forms.ChoiceField(
        choices=models.TranslationSetting.TranslateChoices,
        required=False,
    )
    word_count = forms.IntegerField(required=False)
