"""English language rule forms."""

from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Div, Layout, Row, Submit
from django import forms
from django.db import transaction
from django.urls import reverse_lazy

from apps.core import models as core_models

from .. import models


class RuleForm(forms.ModelForm):  # type: ignore[type-arg]
    """English language rule forms."""

    class Meta:
        """From configuration."""

        model = models.Rule
        fields = [
            'title',
            'description',
            'source',
            'tag',
            'code',
            'title',
        ]


class RuleExampleForm(forms.ModelForm):  # type: ignore[type-arg]
    """Rule examples form."""

    MAX_WORD_LENGTH = models.AbstractWordModel.WORD_LENGTH

    question_english_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Английское слово (вопрос)'
    )
    question_native_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Родное слово (вопрос)'
    )
    answer_english_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Английское слово (ответ)'
    )
    answer_native_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Родное слово (ответ)'
    )

    class Meta:
        """Form configuration."""

        model = models.Rule
        fields = ['title']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)
        form_action = reverse_lazy(
            'lang:english_rule_edit_example', kwargs={'pk': self.instance.pk}
        )

        # Rule clause choice field
        self.fields['clause'] = forms.ModelChoiceField(
            queryset=models.RuleClause.objects.filter(rule=self.instance),
            label='Пункт правила',
        )
        self.fields['example_type'] = forms.ChoiceField(
            choices=models.EnglishRuleExample.ExampleType,
            label='Пример / Исключение',
        )
        self.fields['source'] = forms.ModelChoiceField(
            queryset=core_models.Source.objects.filter(
                user=self.instance.user
            ),
            label='Источник',
            required=False,
        )
        self.fields['question_marks'] = forms.ModelMultipleChoiceField(
            queryset=models.LangMark.objects.filter(
                user=self.instance.user,
            ),
            label='Маркировка вопроса',
            required=False,
        )
        self.fields['answer_marks'] = forms.ModelMultipleChoiceField(
            queryset=models.LangMark.objects.filter(
                user=self.instance.user,
            ),
            label='Маркировка ответа',
            required=False,
        )

        # Crispy form helper
        self.helper = FormHelper()
        self.helper.form_action = form_action
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-md-3'
        # self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            'title',
            'clause',
            Row(
                Column('source'),
                Column('example_type'),
            ),
            Row(
                Column(
                    HTML('<p class="h4 text-center">Вопрос</p>'),
                    'question_marks',
                    'question_english_word',
                    'question_native_word',
                ),
                Column(
                    HTML('<p class="h4 text-center">Ответ</p>'),
                    'answer_marks',
                    'answer_english_word',
                    'answer_native_word',
                ),
            ),
            Div(
                Submit('submit', 'Сохранить', css_class='wse-btn'),
                css_class='d-flex justify-content-end pt-3',
            ),
        )

    # HACK: Fix user getting
    @transaction.atomic
    def save(self, commit: bool = True) -> models.Rule:
        """Save."""
        rule = super().save(commit=False)

        if commit:
            rule.save()
            user = rule.user

            # Native and english words
            question_eng_word, _ = models.EnglishWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['question_english_word'],
            )
            question_native_word, _ = models.NativeWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['question_native_word'],
            )
            answer_eng_word, _ = models.EnglishWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['answer_english_word'],
            )
            answer_native_word, _ = models.NativeWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['answer_native_word'],
            )

            # Word translations
            question_translation, _ = (
                models.EnglishTranslation.objects.get_or_create(
                    user=user,
                    native=question_native_word,
                    english=question_eng_word,
                    source=self.cleaned_data['source'],
                )
            )
            for mark in self.cleaned_data.get('question_marks', []):
                if mark.user == user:
                    models.EnglishMark.objects.get_or_create(
                        user=user,
                        translation=question_translation,
                        mark=mark,
                    )
            answer_translation, _ = (
                models.EnglishTranslation.objects.get_or_create(
                    user=user,
                    native=answer_native_word,
                    english=answer_eng_word,
                    source=self.cleaned_data['source'],
                )
            )
            for mark in self.cleaned_data.get('answer_marks', []):
                if mark.user == user:
                    models.EnglishMark.objects.get_or_create(
                        user=user,
                        translation=answer_translation,
                        mark=mark,
                    )

            # Rule case translation examples
            _ = models.EnglishRuleExample.objects.get_or_create(
                clause=self.cleaned_data['clause'],
                example_type=self.cleaned_data['example_type'],
                question_translation=question_translation,
                answer_translation=answer_translation,
                user=user,
            )

        return rule


class RuleExceptionForm(forms.ModelForm):  # type: ignore[type-arg]
    """Rule exception form."""

    MAX_WORD_LENGTH = models.AbstractWordModel.WORD_LENGTH

    question_english_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Английское слово (вопрос)'
    )
    question_native_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Родное слово (вопрос)'
    )
    answer_english_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Английское слово (ответ)'
    )
    answer_native_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Родное слово (ответ)'
    )

    class Meta:
        """Form configuration."""

        model = models.Rule
        fields = ['title']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)
        form_action = reverse_lazy(
            'lang:english_rule_edit_exception', kwargs={'pk': self.instance.pk}
        )

        self.fields['source'] = forms.ModelChoiceField(
            queryset=core_models.Source.objects.filter(
                user=self.instance.user
            ),
            label='Источник',
            required=False,
        )
        self.fields['question_marks'] = forms.ModelMultipleChoiceField(
            queryset=models.LangMark.objects.filter(
                user=self.instance.user,
            ),
            label='Маркировка вопроса',
            required=False,
        )
        self.fields['answer_marks'] = forms.ModelMultipleChoiceField(
            queryset=models.LangMark.objects.filter(
                user=self.instance.user,
            ),
            label='Маркировка ответа',
            required=False,
        )

        # Crispy form helper
        self.helper = FormHelper()
        self.helper.form_action = form_action
        self.helper.layout = Layout(
            'title',
            'source',
            Row(
                Column(
                    HTML('<p class="h4 text-center">Вопрос</p>'),
                    'question_marks',
                    'question_english_word',
                    'question_native_word',
                ),
                Column(
                    HTML('<p class="h4 text-center">Ответ</p>'),
                    'answer_marks',
                    'answer_english_word',
                    'answer_native_word',
                ),
            ),
            Div(
                Submit('submit', 'Сохранить', css_class='wse-btn'),
                css_class='d-flex justify-content-end pt-3',
            ),
        )

    # HACK: Fix user getting
    @transaction.atomic
    def save(self, commit: bool = True) -> models.Rule:
        """Save."""
        rule = super().save(commit=False)

        if commit:
            rule.save()
            user = rule.user

            # Native and english words
            question_eng_word, _ = models.EnglishWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['question_english_word'],
            )
            question_native_word, _ = models.NativeWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['question_native_word'],
            )
            answer_eng_word, _ = models.EnglishWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['answer_english_word'],
            )
            answer_native_word, _ = models.NativeWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['answer_native_word'],
            )

            # Word translations
            question_translation, _ = (
                models.EnglishTranslation.objects.get_or_create(
                    user=user,
                    native=question_native_word,
                    english=question_eng_word,
                    source=self.cleaned_data['source'],
                )
            )
            for mark in self.cleaned_data.get('question_marks', []):
                if mark.user == user:
                    models.EnglishMark.objects.get_or_create(
                        user=user,
                        translation=question_translation,
                        mark=mark,
                    )
            answer_translation, _ = (
                models.EnglishTranslation.objects.get_or_create(
                    user=user,
                    native=answer_native_word,
                    english=answer_eng_word,
                    source=self.cleaned_data['source'],
                )
            )
            for mark in self.cleaned_data.get('answer_marks', []):
                if mark.user == user:
                    models.EnglishMark.objects.get_or_create(
                        user=user,
                        translation=answer_translation,
                        mark=mark,
                    )

            # Rule case translation examples
            _ = models.EnglishRuleException.objects.get_or_create(
                rule=self.instance,
                question_translation=question_translation,
                answer_translation=answer_translation,
                user=user,
            )

        return rule
