"""English language rule forms."""

from crispy_forms.helper import FormHelper  # type: ignore[import-untyped]
from crispy_forms.layout import (  # type: ignore[import-untyped]
    HTML,
    Column,
    Layout,
    Row,
)
from django import forms
from django.db import transaction
from django.urls import reverse

from apps.core import models as core_models
from apps.core.forms import layouts
from apps.lang.models.abstract import AbstractWordModel
from apps.users.models import Mentorship, Person

from .. import models
from .fields import (
    create_clause_field,
    create_example_type_field,
    create_marks_field,
    create_source_field,
)
from .queries import (
    get_foreign,
    get_native,
)

__all__ = [
    'RuleForm',
    'ClauseForm',
    'TaskExampleForm',
    'WordExampleForm',
    'RuleExceptionForm',
    'RuleAssignmentForm',
]


class _WordExampleFieldsMixin(forms.Form):
    """Provides fields for translation."""

    MAX_WORD_LENGTH = AbstractWordModel.WORD_LENGTH

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
            'title': forms.Textarea(attrs={'rows': 2}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        self.user = kwargs.pop('user', None)
        form_action = kwargs.pop('form_action', None)
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]

        self.helper = FormHelper()
        self.helper.form_id = 'rule-form'
        self.helper.form_action = form_action
        self.helper.layout = Layout(
            'title',
            'description',
            'source',
            Row(Column('tag'), Column('code')),
            layouts.create_button_row(self.helper.form_id),
        )

    def save(self, commit: bool = True) -> models.Rule:
        """Add user to model."""
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance  # type: ignore[no-any-return]


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

        self.fields['parent'].queryset = models.RuleClause.objects.filter(  # type: ignore[attr-defined, misc]
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


class TaskExampleForm(_WordExampleFieldsMixin, forms.Form):
    """Rule examples form."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        self.pk = kwargs.pop('pk', None)
        if not isinstance(self.pk, int):
            raise TypeError('Expected `int` type')

        user = kwargs.pop('user', None)
        if not isinstance(user, Person):
            raise TypeError('Expected `Person` type')
        self.user = user

        form_action = kwargs.pop('form_action', None)
        if form_action is None:
            raise AttributeError('Expected form action')

        super().__init__(*args, **kwargs)  # type: ignore

        self.fields['clause'] = create_clause_field(user, self.pk)
        self.fields['example_type'] = create_example_type_field()
        self.fields['source'] = create_source_field(user)
        self.fields['question_marks'] = create_marks_field(user)
        self.fields['answer_marks'] = create_marks_field(user)

        self.helper = FormHelper()
        self.helper.form_id = 'task-example-form'
        self.helper.form_action = form_action
        self.helper.layout = Layout(
            'clause',
            Row(Column('source'), Column('example_type')),
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

    @transaction.atomic
    def save(self, commit: bool = True) -> models.RuleTaskExample:
        """Save."""
        user = self.user
        data = self.cleaned_data

        question_eng_word = get_foreign(user, data['question_foreign_word'])
        question_native_word = get_native(user, data['question_native_word'])
        answer_eng_word = get_foreign(user, data['answer_foreign_word'])
        answer_native_word = get_native(user, data['answer_native_word'])

        question_translation, _ = (
            models.EnglishTranslation.objects.get_or_create(
                user=user,
                native=question_native_word,
                foreign=question_eng_word,
                source=data['source'],
            )
        )
        for mark in data.get('question_marks', []):
            if mark.user == user:
                models.TranslationMark.objects.get_or_create(
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
                models.TranslationMark.objects.get_or_create(
                    user=user,
                    translation=answer_translation,
                    mark=mark,
                )

        rule_example, _ = models.RuleTaskExample.objects.get_or_create(
            clause=data['clause'],
            example_type=data['example_type'],
            question_translation=question_translation,
            answer_translation=answer_translation,
            user=user,
        )

        return rule_example


class WordExampleForm(forms.Form):
    """Clause rule translation examples form."""

    MAX_WORD_LENGTH = AbstractWordModel.WORD_LENGTH

    foreign_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Английское слово (вопрос)'
    )
    native_word = forms.CharField(
        max_length=MAX_WORD_LENGTH, label='Родное слово (вопрос)'
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        self.pk = kwargs.pop('pk', None)
        if not isinstance(self.pk, int):
            raise TypeError('Expected `int` type')

        user = kwargs.pop('user', None)
        if not isinstance(user, Person):
            raise TypeError('Expected `Person` type')
        self.user = user

        form_action = kwargs.pop('form_action', None)
        super().__init__(*args, **kwargs)  # type: ignore

        self.fields['clause'] = create_clause_field(user, self.pk)
        self.fields['example_type'] = create_example_type_field()
        self.fields['source'] = create_source_field(user)
        self.fields['marks'] = create_marks_field(user)

        self.helper = FormHelper()
        self.helper.form_id = 'word-example-form'
        self.helper.form_action = form_action
        self.helper.layout = Layout(
            'clause',
            Row(
                Column('source', 'example_type'),
                Column('marks'),
            ),
            Column('foreign_word', 'native_word'),
            layouts.create_button_row(self.helper.form_id),
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
                models.TranslationMark.objects.get_or_create(
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


class RuleExceptionForm(_WordExampleFieldsMixin, forms.ModelForm):  # type: ignore[type-arg]
    """Rule exception form."""

    class Meta:
        """Form configuration."""

        model = models.Rule
        fields = ['title']

    def __init__(self, *args: object, **kwargs: object) -> None:
        """Construct the form."""
        super().__init__(*args, **kwargs)  # type: ignore[arg-type]
        form_action = reverse(
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
            queryset=models.Mark.objects.filter(
                user=self.instance.user,
            ),
            label='Маркировка вопроса',
            required=False,
        )
        self.fields['answer_marks'] = forms.ModelMultipleChoiceField(
            queryset=models.Mark.objects.filter(
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
        data = self.cleaned_data

        if commit:
            rule.save()
            user = rule.user

            # Word translations
            question_translation, _ = (
                models.EnglishTranslation.objects.get_or_create(
                    user=user,
                    native=get_native(user, data['question_native_word']),
                    foreign=get_foreign(user, data['question_foreign_word']),
                    source=self.cleaned_data['source'],
                )
            )
            for mark in self.cleaned_data.get('question_marks', []):
                if mark.user == user:
                    models.TranslationMark.objects.get_or_create(
                        user=user,
                        translation=question_translation,
                        mark=mark,
                    )
            answer_translation, _ = (
                models.EnglishTranslation.objects.get_or_create(
                    user=user,
                    native=get_native(user, data['answer_native_word']),
                    foreign=get_foreign(user, data['answer_foreign_word']),
                    source=self.cleaned_data['source'],
                )
            )
            for mark in self.cleaned_data.get('answer_marks', []):
                if mark.user == user:
                    models.TranslationMark.objects.get_or_create(
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

        form_action = reverse(
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
        self.helper.form_id = 'assigned-form'
        self.helper.layout = Layout(
            'mentorship',
            'rule',
            layouts.create_button_row(self.helper.form_id),
        )
