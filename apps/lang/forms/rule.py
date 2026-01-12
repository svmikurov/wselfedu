"""English language rule forms."""

from crispy_forms.helper import FormHelper  # type: ignore[import-untyped]
from crispy_forms.layout import (  # type: ignore[import-untyped]
    HTML,
    Column,
    Div,
    Layout,
    Row,
    Submit,
)
from django import forms
from django.db import transaction
from django.urls import reverse_lazy, reverse

from apps.core import models as core_models
from apps.users.models import Mentorship

from .. import models
from . import layouts


class TranslationExampleFieldsMixin:
    """Provides fields for translation."""

    MAX_WORD_LENGTH = models.AbstractWordModel.WORD_LENGTH

    question_foreign_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Английское слово (вопрос)'
    )
    question_native_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Родное слово (вопрос)'
    )
    answer_foreign_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Английское слово (ответ)'
    )
    answer_native_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Родное слово (ответ)'
    )


class RuleForm(forms.ModelForm):  # type: ignore[type-arg]
    """Rule forms."""

    class Meta:
        """From configuration."""

        model = models.Rule
        fields = [
            'title',
            'description',
            'source',
            'tag',
            'code',
        ]
        widgets = {
            'title': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

        self.helper = FormHelper()
        self.helper.form_id = 'rule-form'
        self.helper.layout = Layout(
            'title',
            'description',
            'source',
            Row(Column('tag'), Column('code')),
            layouts.create_button_row(self.helper.form_id),
        )


class ClauseForm(forms.ModelForm):  # type: ignore[type-arg]
    """Rule clause forms."""

    class Meta:
        """From configuration."""

        model = models.RuleClause
        fields = [
            'rule',
            'parent',
            'ordinal',
            'content',
            'exception_content',
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'exception_content': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        self.user = kwargs.pop('user', None)
        rule = kwargs.pop('rule', None)
        form_action = kwargs.pop('form_action', None)
        super().__init__(*args, **kwargs)  # type: ignore

        if rule:
            self.initial['rule'] = rule

        self.fields['parent'].queryset = models.RuleClause.objects.filter(  # type: ignore[attr-defined]
            rule=rule,
            parent=None,
        )

        self.helper = FormHelper()
        self.helper.form_id = 'clause-form'
        self.helper.form_action = form_action
        self.helper.layout = Layout(
            'rule',
            'parent',
            'ordinal',
            'content',
            'exception_content',
            layouts.create_button_row(self.helper.form_id),
        )

    def save(self, commit: bool = True) -> models.RuleClause:
        """Save rule clause."""
        clause = super().save(commit=False)
        clause.validate_depth()
        clause.user = self.user
        if commit:
            clause.save()
            self.save_m2m()
        return clause  # type: ignore[no-any-return]


class ClauseExampleForm(forms.ModelForm):  # type: ignore[type-arg]
    """Rule examples form."""

    MAX_WORD_LENGTH = models.AbstractWordModel.WORD_LENGTH

    question_foreign_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Английское слово (вопрос)'
    )
    question_native_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Родное слово (вопрос)'
    )
    answer_foreign_word = forms.CharField(
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
        self.user = kwargs.pop('user', None)
        rule = kwargs.pop('rule', None)
        super().__init__(*args, **kwargs)  # type: ignore

        form_action = reverse(
            'lang:english_rule_edit_example',
            kwargs={'pk': rule.pk},
        )

        self.initial['title'] = rule
        
        # Rule clause choice field
        self.fields['clause'] = forms.ModelChoiceField(
            queryset=models.RuleClause.objects.filter(rule=rule),
            label='Пункт правила',
        )
        self.fields['example_type'] = forms.ChoiceField(
            choices=models.RuleTaskExample.ExampleType,
            label='Пример / Исключение',
        )
        self.fields['source'] = forms.ModelChoiceField(
            queryset=core_models.Source.objects.filter(
                user=self.user
            ),
            label='Источник',
            required=False,
        )
        self.fields['question_marks'] = forms.ModelMultipleChoiceField(
            queryset=models.LangMark.objects.filter(
                user=self.user,
            ),
            label='Маркировка вопроса',
            required=False,
        )
        self.fields['answer_marks'] = forms.ModelMultipleChoiceField(
            queryset=models.LangMark.objects.filter(
                user=self.user,
            ),
            label='Маркировка ответа',
            required=False,
        )

        self.helper = FormHelper()
        self.helper.form_action = form_action
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
                    'question_foreign_word',
                    'question_native_word',
                ),
                Column(
                    HTML('<p class="h4 text-center">Ответ</p>'),
                    'answer_marks',
                    'answer_foreign_word',
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

            # Native and foreign words
            question_eng_word, _ = models.EnglishWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['question_foreign_word'],
            )
            question_native_word, _ = models.NativeWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['question_native_word'],
            )
            answer_eng_word, _ = models.EnglishWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['answer_foreign_word'],
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
                    foreign=question_eng_word,
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
                    foreign=answer_eng_word,
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
            _, _ = models.RuleTaskExample.objects.get_or_create(
                clause=self.cleaned_data['clause'],
                example_type=self.cleaned_data['example_type'],
                question_translation=question_translation,
                answer_translation=answer_translation,
                user=user,
            )

        return rule  # type: ignore[no-any-return]

class ClauseTranslationForm(forms.Form):  # type: ignore[type-arg]
    """Clause rule translation examples form."""

    MAX_WORD_LENGTH = models.AbstractWordModel.WORD_LENGTH

    foreign_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Английское слово (вопрос)'
    )
    native_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Родное слово (вопрос)'
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        self.user = kwargs.pop('user', None)
        # Available rule clauses are filtered by the rule
        rule = kwargs.pop('rule', None)
        super().__init__(*args, **kwargs)  # type: ignore

        form_action = reverse(
            'lang:english_rule_edit_example',
            kwargs={'pk': rule.pk},
        )

        # Rule clause choice field
        self.fields['clause'] = forms.ModelChoiceField(
            queryset=models.RuleClause.objects.filter(rule=rule),
            label='Пункт правила',
        )
        self.fields['example_type'] = forms.ChoiceField(
            choices=models.RuleTaskExample.ExampleType,
            label='Пример / Исключение',
        )
        self.fields['source'] = forms.ModelChoiceField(
            queryset=core_models.Source.objects.filter(
                user=self.user
            ),
            label='Источник',
            required=False,
        )
        self.fields['marks'] = forms.ModelMultipleChoiceField(
            queryset=models.LangMark.objects.filter(
                user=self.user,
            ),
            label='Маркировка вопроса',
            required=False,
        )

        self.helper = FormHelper()
        self.helper.form_action = form_action
        self.helper.layout = Layout(
            'clause',
            Row(
                Column('source'),
                Column('example_type'),
            ),
            'foreign_word',
            'native_word',
            Div(
                Submit('submit', 'Сохранить', css_class='wse-btn'),
                css_class='d-flex justify-content-end pt-3',
            ),
        )

    @transaction.atomic
    def save(self) -> models.RuleExample:
        """Save the form data and create related objects."""
        user = self.user
        cleaned_data = self.cleaned_data

        # Native and foreign words
        foreign_word, _ = models.EnglishWord.objects.get_or_create(
            user=user,
            word=cleaned_data['foreign_word'],
        )
        native_word, _ = models.NativeWord.objects.get_or_create(
            user=user,
            word=cleaned_data['native_word'],
        )
        
        # Word translations
        translation, _ = models.EnglishTranslation.objects.get_or_create(
            user=user,
            native=native_word,
            foreign=foreign_word,
            source=cleaned_data['source'],
        )
        
        # Add marks if any
        for mark in cleaned_data.get('marks', []):
            if mark.user == user:
                models.EnglishMark.objects.get_or_create(
                    user=user,
                    translation=translation,
                    mark=mark,
                )

        # Create and return RuleExample
        rule_example, _ = models.RuleExample.objects.get_or_create(
            clause=cleaned_data['clause'],
            translation=translation,
            example_type=cleaned_data['example_type'],
            user=user,
        )
        
        return rule_example


class RuleExceptionForm(forms.ModelForm):  # type: ignore[type-arg]
    """Rule exception form."""

    MAX_WORD_LENGTH = models.AbstractWordModel.WORD_LENGTH

    question_foreign_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Английское слово (вопрос)'
    )
    question_native_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Родное слово (вопрос)'
    )
    answer_foreign_word = forms.CharField(
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
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
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
        self.helper.form_id = 'exception-form'
        self.helper.layout = Layout(
            'title',
            'source',
            Row(
                Column(
                    HTML('<p class="h4 text-center">Вопрос</p>'),
                    'question_marks',
                    'question_foreign_word',
                    'question_native_word',
                ),
                Column(
                    HTML('<p class="h4 text-center">Ответ</p>'),
                    'answer_marks',
                    'answer_foreign_word',
                    'answer_native_word',
                ),
            ),
            layouts.create_button_row(self.helper.form_id),
        )

    # HACK: Fix user getting
    @transaction.atomic
    def save(self, commit: bool = True) -> models.Rule:
        """Save."""
        rule = super().save(commit=False)

        if commit:
            rule.save()
            user = rule.user

            # Native and foreign words
            question_eng_word, _ = models.EnglishWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['question_foreign_word'],
            )
            question_native_word, _ = models.NativeWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['question_native_word'],
            )
            answer_eng_word, _ = models.EnglishWord.objects.get_or_create(
                user=user,
                word=self.cleaned_data['answer_foreign_word'],
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
                    foreign=question_eng_word,
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
                    foreign=answer_eng_word,
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
            _ = models.EnglishRuleException.objects.get_or_create(  # type: ignore[attr-defined]
                rule=self.instance,
                question_translation=question_translation,
                answer_translation=answer_translation,
                user=user,
            )

        return rule  # type: ignore[no-any-return]


class RuleAssignmentForm(forms.ModelForm):  # type: ignore[type-arg]
    """Rule assignation form for mentorship."""

    class Meta:
        """Form configuration."""

        model = models.MentorshipEnglishRule
        fields = ['mentorship', 'rule']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        user = kwargs.pop('user')
        rule = kwargs.pop('rule')
        super().__init__(*args, **kwargs)  # type: ignore

        form_action = reverse_lazy(
            'lang:english_rule_assignment_create',
            kwargs={'pk': rule.pk},  # type: ignore[attr-defined]
        )

        mentorships = Mentorship.objects.select_related(  # type: ignore[misc]
            'student', 'mentor'
        ).filter(mentor=user)

        self.fields['mentorship'].queryset = mentorships  # type: ignore[attr-defined]

        if rule:
            self.initial['rule'] = rule

        self.helper = FormHelper()
        self.helper.form_action = form_action
        self.helper.form_id = 'exception-form'
        self.helper.layout = Layout(
            'mentorship',
            'rule',
            layouts.create_button_row(self.helper.form_id),
        )
