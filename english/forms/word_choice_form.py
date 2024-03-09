from crispy_forms.bootstrap import InlineCheckboxes
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, HTML, Row, Column
from django import forms
from django.db.models import Model
from django.urls import reverse_lazy

from english.models import CategoryModel, SourceModel

NOT_CHOISED_FORM_VALUE = 0

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


def create_choices_by_model(model: Model):
    """Создай набор экземпляров модели для отображения в поле выбора формы."""
    choices = []
    queryset = model.objects.all()

    # Создание списка выбора значений поля формы.
    for instance in queryset:
        form_value, choice_name = instance.pk, str(instance)
        choice = (form_value, choice_name)
        choices.append(choice)

    # Добавление наименование модели в список выбора значений поля формы.
    form_value, model_name = NOT_CHOISED_FORM_VALUE, model._meta.verbose_name
    not_choised = (form_value, model_name)
    choices.append(not_choised)

    return choices


class WordChoiceHelperForm(forms.Form):
    """Форма получения параметров выборки слов для упражнения изучения слов."""

    favorites = forms.BooleanField(
        required=False,
    )
    category = forms.TypedChoiceField(
        choices=create_choices_by_model(CategoryModel),
        initial=NOT_CHOISED_FORM_VALUE,
        required=False,
        label='',
    )
    source = forms.TypedChoiceField(
        choices=create_choices_by_model(SourceModel),
        initial=NOT_CHOISED_FORM_VALUE,
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
            HTML('<label class="h6">Период добавления (изменения)</label>'),
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
