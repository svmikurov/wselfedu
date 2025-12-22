"""Word study parameters model."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final, Self

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from apps.core.models import Period, Source

if TYPE_CHECKING:
    from apps.users.models import Person

    from .. import types


class Parameters(models.Model):
    """Word study parameters model."""

    DEFAULTS: Final[dict[types.Progress, bool]] = {
        'is_study': True,
        'is_repeat': True,
        'is_examine': True,
        'is_know': False,
    }

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_parameters',
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
    progress = models.ForeignKey(
        'study.Progress',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Вариант прогресса',
    )
    is_study = models.BooleanField(
        blank=True,
        null=True,
        default=DEFAULTS['is_study'],
        verbose_name='Изучаю',
        help_text='Выбрать слова для изучения',
    )
    is_repeat = models.BooleanField(
        blank=True,
        null=True,
        default=DEFAULTS['is_repeat'],
        verbose_name='Повторяю',
        help_text='Выбрать слова для повторения',
    )
    is_examine = models.BooleanField(
        blank=True,
        null=True,
        default=DEFAULTS['is_examine'],
        verbose_name='Проверяю',
        help_text='Выбрать слова для проверки',
    )
    is_know = models.BooleanField(
        blank=True,
        null=True,
        default=DEFAULTS['is_know'],
        verbose_name='Знаю',
        help_text='Выбрать выученные слова',
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

        db_table = 'lang_parameters'

        # TODO: Add constrains after Period model improve
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='lang_parameters_unique_user_name',
            ),
        ]

    def obj_to_id_name(self, field: types.OptionT) -> types.IdName | None:
        """Convert object to {id, name} dict."""
        obj = getattr(self, field, None)
        if obj and hasattr(obj, 'id') and hasattr(obj, 'name') and obj.id:
            return {'id': obj.id, 'name': obj.name}
        return None

    def get_progress(self, field: types.Progress) -> bool:
        """Get progress user value if it set or return default."""
        # Check if an attribute exists (for an empty instance)
        attr = getattr(self, field, None)
        return attr if attr is not None else self.DEFAULTS[field]

    @property
    def study(self) -> bool:
        """Is study."""
        return self.get_progress('is_study')

    @property
    def repeat(self) -> bool:
        """Is repeat."""
        return self.get_progress('is_repeat')

    @property
    def examine(self) -> bool:
        """Is examine."""
        return self.get_progress('is_examine')

    @property
    def know(self) -> bool:
        """Is know."""
        return self.get_progress('is_know')

    @classmethod
    def get_instants(cls, user: Person) -> Self:
        """Get user translation parameters or return defaults."""
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            return cls()


class TranslationSetting(models.Model):
    """Translation study settings model."""

    class TranslateChoices(models.TextChoices):
        """Translate order choices."""

        FROM_NATIVE = 'from_native', 'С родного языка'
        TO_NATIVE = 'to_native', 'На родной язык'
        RANDOM = 'random', 'Случайный порядок'

    DEFAULT_TRANSLATION_ORDER = TranslateChoices.TO_NATIVE

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_translation_settings',
    )

    translation_order = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=TranslateChoices.choices,
        default=DEFAULT_TRANSLATION_ORDER,
        verbose_name='Порядок перевода',
    )
    word_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Максимальное количество слов',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлены',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменены',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Настройки изучения переводов'
        verbose_name_plural = 'Настройки изучения переводов'

        db_table = 'lang_translation_settings'

        # TODO: Add constrains after Period model improve
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='lang_translation_settings_unique_user_name',
            ),
        ]

    @property
    def translation_order_display(self) -> str:
        """Get a human-readable translation name."""
        return self.get_translation_order_display()

    @classmethod
    def resolve_order_choice(
        cls, order_value: str | None = None
    ) -> tuple[str, str]:
        """Resolve order choice, return default if None."""
        choice = (
            cls.TranslateChoices(order_value)
            if order_value
            else cls.TranslateChoices.TO_NATIVE
        )
        return choice.value, choice.label

    @classmethod
    def get_instants(cls, user: Person) -> Self:
        """Get user translation settings or return defaults."""
        try:
            instance = cls.objects.get(user=user)
        except cls.DoesNotExist:
            return cls()
        return instance


class PresentationSettings(models.Model):
    """Presentation settings model."""

    MIN_TIMEOUT: Final[int] = 1
    DEFAULT_TIMEOUT: Final[int] = 3
    MAX_TIMEOUT: Final[int] = 300

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_presentation_settings',
    )

    question_timeout = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=DEFAULT_TIMEOUT,
        validators=[
            validators.MinValueValidator(MIN_TIMEOUT),
            validators.MaxValueValidator(MAX_TIMEOUT),
        ],
        verbose_name='Время для вопроса (сек)',
        help_text=f'От {MIN_TIMEOUT} до {MAX_TIMEOUT} секунд',
    )
    answer_timeout = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        default=DEFAULT_TIMEOUT,
        validators=[
            validators.MinValueValidator(MIN_TIMEOUT),
            validators.MaxValueValidator(MAX_TIMEOUT),
        ],
        verbose_name='Время для ответа (сек)',
        help_text=f'От {MIN_TIMEOUT} до {MAX_TIMEOUT} секунд',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлены',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменены',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Настройки презентации'
        verbose_name_plural = 'Настройки презентации'

        db_table = 'lang_presentation_settings'

        # TODO: Add constrains after Period model improve
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='lang_presentation_settings_unique_user_name',
            ),
        ]

    @classmethod
    def get_instants(cls, user: Person) -> Self:
        """Get user presentation settings or return defaults."""
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            return cls()
