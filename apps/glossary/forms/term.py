"""Term form."""

from django import forms

from ..models import Term


class TermForm(forms.ModelForm):  # type: ignore[type-arg]
    """Term form."""

    class Meta:
        """Configure the form."""

        model = Term
        fields = ['name', 'definition']
        widgets = {
            'definition': forms.Textarea(
                attrs={
                    'rows': 4,
                },
            ),
        }
