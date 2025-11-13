"""Native-English translation study progress model."""

from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

MAX_ENGLISH_PROGRESS: int = 12


class EnglishProgress(models.Model):
    """Native-English translation study progress model."""

    MAX_PROGRESS: int = MAX_ENGLISH_PROGRESS

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    translation = models.ForeignKey(
        'EnglishTranslation',
        on_delete=models.CASCADE,
        verbose_name='Перевод родной-английский',
    )
    progress = models.PositiveSmallIntegerField(
        validators=[
            validators.MaxValueValidator(
                MAX_PROGRESS,
                message=(
                    f'Значение прогресса не должно превышать {MAX_PROGRESS}'
                ),
            )
        ],
        verbose_name='Прогресс изучения',
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Добавлено',
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Обновлено',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогресс'

        db_table = 'lang_progress_english'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'translation'],
                name='progress_english_unique_user_translation',
            ),
            models.CheckConstraint(
                condition=models.Q(progress__gte=0)
                & models.Q(progress__lte=MAX_ENGLISH_PROGRESS),
                name='progress_english_range_check',
            ),
        ]
