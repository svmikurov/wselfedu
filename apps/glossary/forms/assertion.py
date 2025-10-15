"""Term assertion form."""

from django import forms

from ..models import TermAssertion


class TermAssertionForm(forms.ModelForm):  # type: ignore[type-arg]
    """Term assertion form."""

    class Meta:
        """Configure the form."""

        model = TermAssertion
        fields = 'term', 'assertion'
        widgets = {
            'assertion': forms.Textarea(
                attrs={
                    'rows': 4,
                }
            ),
        }
