from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Row, Column
from django import forms
from django.urls import reverse_lazy

from english.models import CategoryModel, SourceModel

DEFAULT_CHOICE_VALUE = 0

PERIOD_START = (
    ('DT', 'Сегодня'),
    ('D3', 'Три дня назад'),
    ('W1', 'Неделя назад'),
    ('W4', 'Четыре недели назад'),
    ('NC', 'Не выбран'),
)
PERIOD_END = (
    ('DT', 'Сегодня'),
    ('D3', 'Три дня назад'),
    ('W1', 'Неделя назад'),
    ('W4', 'Четыре недели назад'),
)
DEFAULT_START_PERIOD = 'NC'
DEFAULT_END_PERIOD = 'DT'
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


def create_choices(model, user_id):
    """Create human-readable choice by model and user_id."""
    choices = []
    queryset = model.objects.filter(user_id=user_id)

    # Populate a list of choices.
    for instance in queryset:
        model_value, human_readable_name = instance.pk, str(instance)
        choice = (model_value, human_readable_name)
        choices.append(choice)

    # Add model name to human-readable list as default choice.
    model_name = model._meta.verbose_name
    not_choised = (DEFAULT_CHOICE_VALUE, model_name)
    choices.append(not_choised)

    return choices


def create_category_choice(user_id):
    """Create category choices by ``CategoryModel``."""
    choices = create_choices(CategoryModel, user_id)
    return choices


def create_source_choice(user_id):
    """Create source choices by ``SourceModel``."""
    choices = create_choices(SourceModel, user_id)
    return choices


class WordChoiceHelperForm(forms.Form):
    """Форма получения параметров выборки слов для упражнения изучения слов."""

    def __init__(self, *args, **kwargs):
        self.user_id = kwargs.pop('user_id', None)
        super(WordChoiceHelperForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = create_category_choice(self.user_id)
        self.fields['source'].choices = create_source_choice(self.user_id)

    favorites = forms.BooleanField(
        required=False,
    )
    category = forms.TypedChoiceField(
        initial=DEFAULT_CHOICE_VALUE,
        required=False,
        label='',
    )
    source = forms.TypedChoiceField(
        initial=DEFAULT_CHOICE_VALUE,
        required=False,
        label='',
    )
    period_start_date = forms.ChoiceField(
        choices=PERIOD_START,
        initial=DEFAULT_START_PERIOD,
        required=False,
        label='Начало',
    )
    period_end_date = forms.ChoiceField(
        choices=PERIOD_END,
        initial=DEFAULT_END_PERIOD,
        required=False,
        label='Конец',
    )
    word_count = forms.MultipleChoiceField(
        choices=WORD_COUNT,
        initial=('OW', 'CB'),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='',
    )
    knowledge_assessment = forms.MultipleChoiceField(
        choices=KNOWLEDGE_ASSESSMENT,
        initial='S',
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='',
    )

    @property
    def helper(self):
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
            HTML('<label class="h6">Период добавления</label>'),
            Row(
                Column('period_start_date', css_class='form-group col-sm-6'),
                Column('period_end_date', css_class='form-group col-sm-6'),
                css_class='form-row',
            ),
            HTML('<label class="h6">Слово, длина выражения</label>'),
            InlineCheckboxes('word_count'),
            HTML('<label class="h6">Этап изучения слов</label>'),
            InlineCheckboxes('knowledge_assessment'),
            Submit('submit', 'Начать', css_class='button white'),
        )

        return helper
