"""Foreign translate conditions choice module.

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
    LANGUAGE_ORDER_CHOICE,
    PROGRESS_CHOICES,
    WORD_COUNT_CHOICE,
)
from foreign.models import TranslateParams, WordCategory, WordSource


class ForeignTranslateChoiceForm(forms.Form):
    """Foreign word translation conditions choice form."""

    MODEL_FIELDS = {
        'category': WordCategory,
        'source': WordSource,
    }

    favorites = forms.BooleanField(
        required=False,
        label='Только избранные слова',
    )
    language_order = forms.ChoiceField(
        choices=LANGUAGE_ORDER_CHOICE,
        required=False,
        label='',
    )
    category = forms.TypedChoiceField(
        required=False,
        coerce=int,
        label='',
    )
    source = forms.TypedChoiceField(
        initial=DEFAULT_ZERO_VALUE,
        coerce=int,
        required=False,
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
    word_count = forms.MultipleChoiceField(
        choices=WORD_COUNT_CHOICE[1:],
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='Слово, длина выражения',
    )
    progress = forms.MultipleChoiceField(
        choices=PROGRESS_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='Этап изучения слов',
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
        instance, _ = TranslateParams.objects.get_or_create(user=request.user)
        super(ForeignTranslateChoiceForm, self).__init__(*args, **kwargs)

        for field, model in self.MODEL_FIELDS.items():
            self.fields[field].choices = self._create_choices(model, user_id)
        self.fields['favorites'].initial = instance.favorites
        self.fields['language_order'].initial = instance.language_order
        self.fields['period_start_date'].initial = instance.period_start_date
        self.fields['period_end_date'].initial = instance.period_end_date
        self.fields['word_count'].initial = instance.word_count
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
                    'language_order',
                    css_class='col-6',
                    data_testid='language_order',
                ),
            ),
            Row(
                Column('category', css_class='col-6'),
                Column('source', css_class='col-6'),
            ),
            Row(
                HTML('<label class="h6">Период добавления слова</label>'),
                Column('period_start_date', css_class='col-6'),
                Column('period_end_date', css_class='col-6'),
                data_testid='word_addition_period',
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
            InlineCheckboxes('word_count', data_testid='word_count'),
        )  # fmt: skip

        return helper
