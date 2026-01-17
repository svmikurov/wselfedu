"""Language rules models."""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

# REVIEW: Review models methods/properties
# after completing the formation of business logic


class ExampleType(models.TextChoices):
    """Example type enumeration."""

    EXAMPLE = 'example', 'Пример'
    EXCEPTION = 'exception', 'Исключение'


class Rule(models.Model):
    """Language rule model."""

    title = models.CharField(
        max_length=255,
        verbose_name='Правило',
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Описание правила',
    )
    source = models.ForeignKey(
        'core.Source',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Источник правила',
    )

    tag = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Тег правила',
    )
    code = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        verbose_name='Код правила',
        help_text='Уникальный буквенно-цифровой код (например, PROC-001)',
    )

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Пользователь добавивший правило',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Правило пользователя'
        verbose_name_plural = 'Правила пользователя'

        ordering = ['created_at']

        db_table = 'lang_rule'

    def __str__(self) -> str:
        """Return the string representation."""
        return str(self.title)

    def get_absolute_url(self) -> str:
        """Get rule detail url path."""
        return reverse('lang:english_rule_detail', kwargs={'pk': self.pk})


class RuleClause(models.Model):
    """Model for storing clauses and subclauses of rules.

    Recursive structure.
    """

    rule = models.ForeignKey(
        Rule,
        on_delete=models.CASCADE,
        related_name='clauses',
        verbose_name='Правило',
    )

    # Recursive relationship for nesting
    # (item -> subitem -> sub-subitem)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True,
        verbose_name='Родительский пункт',
    )

    # The ordinal number within the parent element
    # (or rule, if parent=None)
    ordinal = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Порядковый номер',
    )
    content = models.TextField(
        verbose_name='Содержание',
    )
    exception_content = models.TextField(
        null=True,
        blank=True,
        verbose_name='Исключение пункта правила',
    )

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Пользователь (собственник) добавивший пункт',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Пункт правила'
        verbose_name_plural = 'Пункты правил'

        ordering = ['rule', 'ordinal', 'created_at']
        unique_together = [['rule', 'content']]

        db_table = 'lang_rule_clause'

    def __str__(self) -> str:
        """Return the string representation."""
        return str(self.content)

    def validate_depth(self) -> None:
        """Validate clause depth.

        Raises validation error if parent has parent.
        """
        if self.parent and self.parent.parent:
            raise ValidationError(
                'Maximum one level of nesting.'
                'You cannot create sub-items within sub-items.'
            )


class RuleException(models.Model):
    """Rule exception."""

    rule = models.ForeignKey(
        Rule,
        on_delete=models.CASCADE,
        related_name='exceptions',
        verbose_name='Правило',
    )
    question_translation = models.ForeignKey(
        'EnglishTranslation',
        on_delete=models.CASCADE,
        related_name='exception_question_translation',
        verbose_name='Перевод вопроса',
    )
    answer_translation = models.ForeignKey(
        'EnglishTranslation',
        on_delete=models.CASCADE,
        related_name='exception_answer_translation',
        verbose_name='Перевод ответа',
    )

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Пользователь, добавивший исключение',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Исключение правила'
        verbose_name_plural = 'Исключения правил'

        ordering = ['rule', 'created_at']
        unique_together = [
            ['question_translation', 'answer_translation'],
        ]

        db_table = 'lang_rule_exception'

    @property
    def question_in_foreign(self) -> str:
        """Get the question in foreign language."""
        return str(self.question_translation.foreign.word)

    @property
    def answer_in_foreign(self) -> str:
        """Get the answer in foreign language."""
        return str(self.answer_translation.foreign.word)

    @property
    def task(self) -> str:
        """Get the task in a foreign language."""
        return f'{self.question_in_foreign} - {self.answer_in_foreign}'


class RuleTaskExample(models.Model):
    """Language rule clause task example/exception."""

    clause = models.ForeignKey(
        'RuleClause',
        on_delete=models.CASCADE,
        related_name='rule_task_examples',
        verbose_name='Пункт правила языка',
    )

    question_translation = models.ForeignKey(
        'EnglishTranslation',
        on_delete=models.CASCADE,
        related_name='task_rule_questions',
        verbose_name='Перевод вопроса',
    )
    answer_translation = models.ForeignKey(
        'EnglishTranslation',
        on_delete=models.CASCADE,
        related_name='task_rule_answers',
        verbose_name='Перевод ответа',
    )

    example_type = models.CharField(
        max_length=10,
        choices=ExampleType.choices,
        default=ExampleType.EXAMPLE,
        verbose_name='Тип примера',
        help_text='Тип примера пункта правила: "пример"/"исключение"',
    )

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Пользователь, добавивший пример/исключение',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Пример/исключение задания пункта правила'
        verbose_name_plural = 'Примеры/исключения заданий пунктов правил'

        ordering = ['clause', 'created_at']
        unique_together = [
            ['clause', 'question_translation', 'answer_translation'],
        ]

        db_table = 'lang_rule_task_example'

    def __str__(self) -> str:
        """Get the string representation of task example."""
        return (
            f'{self.question_translation.foreign.word} - '
            f'{self.answer_translation.foreign.word}'
        )

    @property
    def question_in_foreign(self) -> str:
        """Get the question in foreign language."""
        return str(self.question_translation.foreign.word)

    @property
    def answer_in_foreign(self) -> str:
        """Get the answer in foreign language."""
        return str(self.answer_translation.foreign.word)

    @property
    def task(self) -> str:
        """Get the task in a foreign language."""
        return f'{self.question_in_foreign} - {self.answer_in_foreign}'


class RuleExample(models.Model):
    """Language rule clause word translation example/exception."""

    clause = models.ForeignKey(
        'RuleClause',
        on_delete=models.CASCADE,
        related_name='rule_translation_examples',
        verbose_name='Пункт правила языка',
    )

    translation = models.ForeignKey(
        'EnglishTranslation',
        on_delete=models.CASCADE,
        related_name='translation_rule_examples',
        verbose_name='Перевод вопроса',
    )

    example_type = models.CharField(
        max_length=10,
        choices=ExampleType.choices,
        default=ExampleType.EXAMPLE,
        verbose_name='Тип примера',
        help_text='Тип примера пункта правила: "пример"/"исключение"',
    )

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Пользователь, добавивший пример/исключение',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Пример/исключение слова пункта правила'
        verbose_name_plural = 'Примеры/исключения слов пунктов правил'

        ordering = ['clause', 'created_at']
        unique_together = [
            ['clause', 'translation'],
        ]

        db_table = 'lang_rule_translation_example'

    def __str__(self) -> str:
        """Get the string representation of translation."""
        return f'{self.foreign} - {self.native}'

    @property
    def question_in_foreign(self) -> str:
        """Get the question in foreign language."""
        return str(self.translation.foreign.word)

    @property
    def foreign(self) -> str:
        """Get the string representation of foreign word."""
        return str(self.translation.foreign.word)

    @property
    def native(self) -> str:
        """Get the string representation of native word."""
        return str(self.translation.native.word)
