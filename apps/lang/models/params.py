"""Word study params model."""

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from apps.core.models import Period, Source


class Params(models.Model):
    """Word study default params model."""

    class TranslateChoices(models.TextChoices):
        """Translate order choices."""

        FROM_NATIVE = 'from_native', 'С родного языка'
        TO_NATIVE = 'to_native', 'На родной язык'
        RANDOM = 'random', 'Случайный порядок'

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_params',
    )
    category = models.ForeignKey(
        'LangCategory',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='category_params',
    )
    mark = models.ForeignKey(
        'LangMark',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Маркер',
        related_name='mark_params',
    )
    word_source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Источник',
    )
    translation_order = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=TranslateChoices.choices,
        default=TranslateChoices.TO_NATIVE,
        verbose_name='Порядок перевода',
        help_text='Направление перевода при изучении слов',
    )
    word_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Максимальное количество слов',
    )
    start_period = models.ForeignKey(
        Period,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Период с',
        related_name='after_params',
    )
    end_period = models.ForeignKey(
        Period,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Период до',
        related_name='before_params',
    )
    question_timeout = models.FloatField(
        blank=True,
        null=True,
        validators=[
            validators.MinValueValidator(
                0,
                message='Время не может быть отрицательным',
            ),
        ],
        verbose_name='Время для вопроса (сек)',
    )
    answer_timeout = models.FloatField(
        blank=True,
        null=True,
        validators=[
            validators.MinValueValidator(
                0,
                message='Время не может быть отрицательным',
            ),
        ],
        verbose_name='Время для ответа (сек)',
    )
    is_study = models.BooleanField(
        blank=True,
        null=True,
        default=True,
        verbose_name='Изучаю',
        help_text='Показывать слова для изучения',
    )
    is_repeat = models.BooleanField(
        blank=True,
        null=True,
        default=True,
        verbose_name='Повторяю',
        help_text='Показывать слова для повторения',
    )
    is_examine = models.BooleanField(
        blank=True,
        null=True,
        default=True,
        verbose_name='Проверяю',
        help_text='Показывать слова для проверки',
    )
    is_know = models.BooleanField(
        blank=True,
        null=True,
        default=False,
        verbose_name='Знаю',
        help_text='Показывать изученные слова',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлен',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменен',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Параметр изучения слов'
        verbose_name_plural = 'Параметры изучения слов'

        db_table = 'lang_params'

        # TODO: Add constrains after Period model improve
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='word_study_params_unique_user_name',
            ),
        ]

    @classmethod
    def resolve_order_choice(cls, order_value: str | None) -> tuple[str, str]:
        """Resolve order choice, return default if None."""
        choice = (
            cls.TranslateChoices(order_value)
            if order_value
            else cls.TranslateChoices.TO_NATIVE
        )
        return choice.value, choice.label
