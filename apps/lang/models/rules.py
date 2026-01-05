"""English language rules models."""

from django.db import models


class Rule(models.Model):
    """English language rules models."""

    title = models.CharField(
        max_length=255,
        verbose_name='Правило',
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Описание',
    )
    source = models.ForeignKey(
        'core.Source',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Источник',
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
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Правило'
        verbose_name_plural = 'Правила'

        ordering = ['created_at']

        db_table = 'lang_english_rule'

    def __str__(self) -> str:
        """Return the model string representation."""
        return str(self.title)


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

    example = models.ManyToManyField(  # type: ignore[var-annotated]
        'EnglishTranslation',
        through='EnglishTranslationExample',
        through_fields=('clause', 'translation'),
        related_name='example_rule_clauses',
        blank=True,
        verbose_name='Пример',
        help_text='Пример пункта правила (слово)',
    )
    exception = models.ManyToManyField(  # type: ignore[var-annotated]
        'EnglishTranslation',
        through='EnglishTranslationException',
        through_fields=('clause', 'translation'),
        related_name='exception_rule_clauses',
        blank=True,
        verbose_name='Исключение',
        help_text='Исключение из пункта правила (слово)',
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

        verbose_name = 'Пункт правила'
        verbose_name_plural = 'Пункты правил'

        ordering = ['rule', 'ordinal']
        unique_together = [['rule', 'content']]


class EnglishTranslationExample(models.Model):
    """English rule clause the translation example."""

    clause = models.ForeignKey(
        'RuleClause',
        on_delete=models.CASCADE,
        verbose_name='Пункт правила английского языка',
    )
    translation = models.ForeignKey(
        'EnglishTranslation',
        on_delete=models.CASCADE,
        verbose_name='Пример',
        help_text='Перевод слова, используемого для примера',
    )

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Пользователь добавивший пример',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )


class EnglishTranslationException(models.Model):
    """English rule clause the translation exception."""

    clause = models.ForeignKey(
        'RuleClause',
        on_delete=models.CASCADE,
        verbose_name='Пункт правила английского языка',
    )
    translation = models.ForeignKey(
        'EnglishTranslation',
        on_delete=models.CASCADE,
        verbose_name='Исключение',
        help_text='Перевод слова, используемого для исключения',
    )

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Пользователь добавивший исключение',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления',
    )
