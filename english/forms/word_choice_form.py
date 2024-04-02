"""
Form module for obtaining parameters for choosing words
for word learning exercises.

The form displays words studied by a specific user.
"""

from django import forms
from django.urls import reverse_lazy

from english.models import CategoryModel, SourceModel

from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Row, Column


EDGE_PERIODS = [
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
DEFAULT_START_PERIOD = ('NC', 'Добавлено')
DEFAULT_END_PERIOD = ('DT', 'Сегодня')
WORD_COUNT = (
    ('OW', 'Слово'),
    ('CB', 'Словосочетание'),
    ('PS', 'Часть предложения'),
    ('ST', 'Предложение'),
)
KNOWLEDGE_ASSESSMENT = (
    ('S', 'Изучаю'),        # study
    ('R', 'Повторяю'),      # repeat
    ('E', 'Проверяю'),      # examination
    ('K', 'Знаю'),          # know
)
DEFAULT_KNOWLEDGE_ASSESSMENT = 'S'
DEFAULT_WORD_COUNT = ('OW', 'CB')
DEFAULT_CREATE_CHOICE_VALUE = 0


def create_choices(model, user_id):
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


class WordChoiceHelperForm(forms.Form):
    """Form obtaining word choice parameters for a word learning exercise."""

    # The remaining selection fields do not require specific user.
    only_user_field_choice = {
        'category': CategoryModel,
        'source': SourceModel,
    }

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super(WordChoiceHelperForm, self).__init__(*args, **kwargs)
        for field, model in self.only_user_field_choice.items():
            self.fields[field].choices = create_choices(model, self.user_id)

    favorites = forms.BooleanField(
        required=False,
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
        choices=EDGE_PERIODS,
        initial=DEFAULT_START_PERIOD,
        required=False,
        label='',
    )
    period_end_date = forms.ChoiceField(
        choices=EDGE_PERIODS[:-1],
        initial=DEFAULT_END_PERIOD,
        required=False,
        label='',
    )
    word_count = forms.MultipleChoiceField(
        choices=WORD_COUNT,
        initial=DEFAULT_WORD_COUNT,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='',
    )
    knowledge_assessment = forms.MultipleChoiceField(
        choices=KNOWLEDGE_ASSESSMENT,
        initial=DEFAULT_KNOWLEDGE_ASSESSMENT,
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='',
    )

    @property
    def helper(self):
        """Create form."""
        helper = FormHelper()
        helper.form_method = 'post'
        helper.form_action = reverse_lazy('english:word_choice')

        helper.layout = Layout(
            Field('favorites'),
            Row(
                Column('category', css_class='form-group col-6'),
                Column('source', css_class='form-group col-6'),
                css_class='form-row',
            ),
            HTML('<label class="h6">Период добавления слова</label>'),
            Row(
                Column('period_start_date', css_class='form-group col-6'),
                Column('period_end_date', css_class='form-group col-6'),
                css_class='form-row',
            ),
            HTML('<label class="h6">Слово, длина выражения</label>'),
            InlineCheckboxes('word_count'),
            HTML('<label class="h6">Этап изучения слов</label>'),
            InlineCheckboxes('knowledge_assessment'),
            Submit('submit', 'Начать', css_class='button white'),
        )

        return helper
