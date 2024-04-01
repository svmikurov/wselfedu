from django import forms
from django.forms import TextInput


class CalendarForm(forms.Form):
    date5 = forms.DateField(
        widget=TextInput(attrs={"type": "date"})
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
