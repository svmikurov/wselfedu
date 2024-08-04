from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Field, Layout, Row, Submit
from django import forms

from english.models import CategoryModel, SourceModel

LANGUAGE_ORDER = [
    ('RN', 'Перевод в случайном порядке'),
    ('EN', 'Перевод с английского языка'),
    ('RU', 'Перевод на английский язык'),
]
EDGE_PERIODS_ALIASES = [
    ('DT', 'Сегодня'),
    ('D3', 'Три дня назад'),
    ('W1', 'Неделя назад'),
    ('W2', 'Две недели назад'),
    ('W3', 'Три недели назад'),
    ('W4', 'Четыре недели назад'),
    ('W7', 'Семь недель назад'),
    ('M3', 'Три месяца назад'),
    ('M6', 'Шесть месяцев назад'),
    ('M9', 'Девять месяцев назад'),
    ('NC', 'Добавлено'),
]
"""Edge period aliases at word adding for study
(`list[tuple[str, str]]`).
"""
DEFAULT_START_PERIOD = ('NC', 'Добавлено')
DEFAULT_END_PERIOD = ('DT', 'Сегодня')
WORD_COUNT = (
    ('OW', 'Слово'),
    ('CB', 'Словосочетание'),
    ('PS', 'Часть предложения'),
    ('ST', 'Предложение'),
)
KNOWLEDGE_ASSESSMENT = (
    ('S', 'Изучаю'),  # study
    ('R', 'Повторяю'),  # repeat
    ('E', 'Проверяю'),  # examination
    ('K', 'Знаю'),  # know
)
DEFAULT_LANGUAGE_ORDER = LANGUAGE_ORDER[0]
DEFAULT_KNOWLEDGE_ASSESSMENT = 'S'
DEFAULT_WORD_COUNT = ('OW', 'CB')
DEFAULT_CREATE_CHOICE_VALUE = 0
DEFAULT_TIMEOUT = 5


class EnglishTranslateChoiceForm(forms.Form):
    """English word translation conditions choice form."""

    MODEL_FIELDS = {
        'category': CategoryModel,
        'source': SourceModel,
    }

    def __init__(self, *args, **kwargs):
        """Init user's model instances at form fields."""
        user_id = kwargs.pop('request').user.id
        super(EnglishTranslateChoiceForm, self).__init__(*args, **kwargs)
        for field, model in self.MODEL_FIELDS.items():
            self.fields[field].choices = self._create_choices(model, user_id)

    favorites = forms.BooleanField(
        required=False,
    )
    language_order = forms.ChoiceField(
        choices=LANGUAGE_ORDER,
        initial=DEFAULT_LANGUAGE_ORDER,
        required=False,
        label='',
    )
    category = forms.TypedChoiceField(
        initial=DEFAULT_CREATE_CHOICE_VALUE,
        required=False,
        label='',
    )
    source = forms.TypedChoiceField(
        initial=DEFAULT_CREATE_CHOICE_VALUE,
        required=False,
        label='',
    )
    period_start_date = forms.ChoiceField(
        choices=EDGE_PERIODS_ALIASES,
        initial=DEFAULT_START_PERIOD,
        required=False,
        label='',
    )
    period_end_date = forms.ChoiceField(
        choices=EDGE_PERIODS_ALIASES[:-1],
        initial=DEFAULT_END_PERIOD,
        required=False,
        label='',
    )
    word_count = forms.MultipleChoiceField(
        choices=WORD_COUNT,
        initial=DEFAULT_WORD_COUNT,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='Слово, длина выражения',
    )
    knowledge_assessment = forms.MultipleChoiceField(
        choices=KNOWLEDGE_ASSESSMENT,
        initial=DEFAULT_KNOWLEDGE_ASSESSMENT,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='Этап изучения слов',
    )
    timeout = forms.IntegerField(
        initial=DEFAULT_TIMEOUT,
        label='Время на ответ (сек)',
    )

    def clean(self):
        """Convert `str` to `int` form values."""
        cleaned_data = super().clean()
        cleaned_data['category'] = self._to_int(cleaned_data, 'category')
        cleaned_data['source'] = self._to_int(cleaned_data, 'source')
        return cleaned_data

    @staticmethod
    def _to_int(cleaned_data, field_name):
        """Convert `str` to `int` field value."""
        field_value = cleaned_data.get(field_name)
        return int(field_value) if field_value else field_value

    @staticmethod
    def _create_choices(model, user_id):
        """Create human-readable choice by model and user_id."""
        model_name = model._meta.verbose_name
        default_choice = (DEFAULT_CREATE_CHOICE_VALUE, model_name)
        choices = [default_choice]

        # Populate a list of choices.
        queryset = model.objects.filter(user_id=user_id)
        for instance in queryset:
            model_value, human_readable_name = instance.pk, str(instance)
            choice = (model_value, human_readable_name)
            choices.append(choice)

        return choices

    @property
    def helper(self):
        """Structure the form."""
        helper = FormHelper()
        helper.form_method = 'post'

        helper.layout = Layout(
            Row(
                Column(
                    'favorites', css_class='col-6', data_testid='favorites'
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
            InlineCheckboxes(
                'knowledge_assessment', data_testid='knowledge_assessment'
            ),
            Submit(
                'submit', 'Начать', css_class='btn-sm', data_testid='submit'
            ),
            HTML('<p class="h6 pt-3">Дополнительные опции</p>'),
            Field('timeout', css_class='form-group col-6 w-25'),
            InlineCheckboxes('word_count', data_testid='word_count'),
        )

        return helper
