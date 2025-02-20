"""Form to choice params for Term exercise.

.. todo::
   * add count first and count last param choice;
   * refact the code (try apply ModelForm, );
"""

from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Field, Layout, Row, Submit
from django import forms
from django.db import models

from config.constants import (
    DEFAULT_ZERO_VALUE,
    EDGE_PERIOD_CHOICES,
    PROGRESS_CHOICES,
)
from glossary.models import GlossaryParams, TermCategory, TermSource


class GlossaryParamsForm(forms.Form):
    """Term exercise params choice form."""

    MODEL_FIELDS = {
        'category': TermCategory,
        'source': TermSource,
    }

    favorites = forms.BooleanField(
        required=False,
        label='Только избранные термины',
    )
    category = forms.TypedChoiceField(
        required=False,
        coerce=int,
        label='',
    )
    source = forms.TypedChoiceField(
        initial=DEFAULT_ZERO_VALUE,
        required=False,
        coerce=int,
        label='',
    )
    period_start_date = forms.ChoiceField(
        choices=EDGE_PERIOD_CHOICES,
        required=False,
        label='',
    )
    period_end_date = forms.ChoiceField(
        choices=EDGE_PERIOD_CHOICES[:-1],
        required=False,
        label='',
    )
    progress = forms.MultipleChoiceField(
        choices=PROGRESS_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='Этап изучения термина',
    )
    timeout = forms.IntegerField(
        label='Время на ответ (сек)',
    )
    save_params = forms.BooleanField(
        required=False, initial=False, label='Сохранить параметры выбора'
    )
    """The checkbox, is checked, the exercise parameters will be saved.
    """

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Init user's model instances at form fields."""
        request = kwargs.pop('request')
        user_id = request.user.id
        instance, _ = GlossaryParams.objects.get_or_create(user=request.user)
        super(GlossaryParamsForm, self).__init__(*args, **kwargs)

        for field, model in self.MODEL_FIELDS.items():
            self.fields[field].choices = self._create_choices(model, user_id)
        self.fields['favorites'].initial = instance.favorites
        self.fields['period_start_date'].initial = instance.period_start_date
        self.fields['period_end_date'].initial = instance.period_end_date
        self.fields['progress'].initial = instance.progress
        self.fields['timeout'].initial = instance.timeout
        self.fields['category'].initial = self.get_initial(instance.category)
        self.fields['source'].initial = self.get_initial(instance.source)

    @staticmethod
    def get_initial(field: Field) -> int:
        """Get initial value for choices from instance field."""
        try:
            pk = field.pk
        except AttributeError:
            return 0
        else:
            return pk

    @staticmethod
    def _create_choices(
        model: models.Model,
        user_id: id,
    ) -> list[tuple[int, str]]:
        """Create human-readable choice by model and user_id."""
        model_name = model._meta.verbose_name
        default_choice = (DEFAULT_ZERO_VALUE, model_name)
        choices = [default_choice]

        # Populate a list of choices.
        queryset = model.objects.filter(user_id=user_id)
        for instance in queryset:
            instance_id, human_readable_name = instance.pk, str(instance)
            choice = (instance_id, human_readable_name)
            choices.append(choice)

        return choices

    @property
    def helper(self) -> FormHelper:
        """Structure the form."""
        helper = FormHelper()
        helper.form_method = 'POST'

        helper.layout = Layout(
            Row(
                Column(
                    'favorites',
                    css_class='col-6',
                    data_testid='favorites',
                ),
                Column(
                    css_class='col-6',
                ),
            ),
            Row(
                Column('category', css_class='col-6'),
                Column('source', css_class='col-6'),
            ),
            Row(
                HTML('<label class="h6">Период добавления термина</label>'),
                Column('period_start_date', css_class='col-6'),
                Column('period_end_date', css_class='col-6'),
                data_testid='term_addition_period',
            ),
            InlineCheckboxes('progress', data_testid='progress'),
            Row(
                Column(
                    Submit(
                        'submit',
                        'Начать',
                        css_class='btn-sm',
                        data_testid='submit',
                    ),
                ),
                Column(
                    Field(
                        'save_params',
                    )
                ),
            ),
            HTML('<p class="h6 pt-3">Дополнительные опции</p>'),
            Field('timeout', css_class='form-group col-6 w-25'),
        )

        return helper
