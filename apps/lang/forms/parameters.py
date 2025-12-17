"""Translation study parameters."""

from crispy_forms.helper import FormHelper  # type: ignore[import-untyped]
from crispy_forms.layout import (  # type: ignore[import-untyped]
    Column,
    Field,
    Layout,
    Row,
)
from django import forms
from django.contrib.auth import get_user_model

from .. import models

SWITCH_TEMPLATE = 'fields/checkbox.html'
SWITCH_CLASS = 'form-check-input switch-lg'
STYLE_ATTR = {
    'class': SWITCH_CLASS,
}


class ParametersForm(forms.ModelForm):  # type: ignore[type-arg]
    """Translation study parameters form."""

    class Meta:
        """Form configuration."""

        model = models.Parameters
        fields = [
            'category',
            'word_source',
            'start_period',
            'end_period',
            'mark',
            'progress',
            'is_study',
            'is_repeat',
            'is_examine',
            'is_know',
        ]
        widgets = {
            # Adds <input class="form-check-input switch-lg">
            'is_study': forms.CheckboxInput(attrs=STYLE_ATTR),
            'is_repeat': forms.CheckboxInput(attrs=STYLE_ATTR),
            'is_examine': forms.CheckboxInput(attrs=STYLE_ATTR),
            'is_know': forms.CheckboxInput(attrs=STYLE_ATTR),
        }

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Configure the form."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(Column('category'), Column('word_source')),
            Row(Column('start_period'), Column('end_period')),
            Row(Column('mark'), Column('progress')),
            Row(
                Column(Field('is_study', template=SWITCH_TEMPLATE)),
                Column(Field('is_repeat', template=SWITCH_TEMPLATE)),
            ),
            Row(
                Column(Field('is_examine', template=SWITCH_TEMPLATE)),
                Column(Field('is_know', template=SWITCH_TEMPLATE)),
            ),
        )


class TranslationSettingsForm(forms.ModelForm):  # type: ignore[type-arg]
    """Translation settings form."""

    class Meta:
        """Form configuration."""

        model = models.TranslationSetting
        fields = ['translation_order', 'word_count']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Configure the form helper."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(Column('translation_order'), Column('word_count')),
        )


class PresentationSettingsForm(forms.ModelForm):  # type: ignore[type-arg]
    """Presentation settings form."""

    class Meta:
        """Form configuration."""

        model = models.PresentationSettings
        fields = ['question_timeout', 'answer_timeout']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Configure the form helper."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(Column('question_timeout'), Column('answer_timeout')),
        )


TranslationSettingsFormSet = forms.inlineformset_factory(
    get_user_model(),
    models.TranslationSetting,
    form=TranslationSettingsForm,
    extra=1,
    max_num=1,
    can_delete=False,
    fk_name='user',
    fields=['translation_order', 'word_count'],
)

PresentationSettingsFormSet = forms.inlineformset_factory(
    get_user_model(),
    models.PresentationSettings,
    form=PresentationSettingsForm,
    extra=1,
    max_num=1,
    can_delete=False,
    fk_name='user',
    fields=['question_timeout', 'answer_timeout'],
)
