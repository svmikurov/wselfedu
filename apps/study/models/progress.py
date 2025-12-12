"""Item study progress phase model."""

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q


class Progress(models.Model):
    """Item study progress phase model."""

    # Max progress phase values
    STUDY_DEFAULT = 7
    REPEAT_DEFAULT = 10
    EXAMINE_DEFAULT = 13
    KNOW_DEFAULT = 17

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='progresses',
    )
    name = models.CharField(
        max_length=30,
        help_text='Наименование версии шкалы прогресса',
    )

    study = models.PositiveSmallIntegerField(
        default=STUDY_DEFAULT,
        verbose_name='Изучаю',
        help_text='Значение для смены стадий "Изучаю-Повторяю"',
    )
    repeat = models.PositiveSmallIntegerField(
        default=REPEAT_DEFAULT,
        verbose_name='Повторяю',
        help_text='Значение для смены стадии "Повторяю-Проверяю"',
    )
    examine = models.PositiveSmallIntegerField(
        default=EXAMINE_DEFAULT,
        verbose_name='Проверяю',
        help_text='Значение для смены стадии "Проверяю-Знаю"',
    )
    know = models.PositiveSmallIntegerField(
        default=KNOW_DEFAULT,
        verbose_name='Знаю',
        help_text='Максимальное значение прогресса',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменено',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Прогресс изучения'
        verbose_name_plural = 'Прогрессы изучения'

        db_table = 'study_progress'

        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['user']),
        ]

        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(study__lt=F('repeat'))
                    & Q(repeat__lt=F('examine'))
                    & Q(examine__lt=F('know'))
                ),
                name='progress_study_lt_repeat_lt_examine_lt_know',
            ),
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_user_progress_name',
            ),
        ]

    def __str__(self) -> str:
        """Get string representation of progress instance."""
        return str(self.name)

    def clean(self) -> None:
        """Validate progress values on model level."""
        super().clean()

        if not (self.study < self.repeat < self.examine < self.know):
            raise ValidationError(
                {
                    'study': 'study < repeat',
                    'repeat': 'repeat < examine',
                    'examine': 'examine < know',
                    'know': 'Values ​​should increase from left to right',
                }
            )

        if (
            self.study < 0
            or self.repeat < 0
            or self.examine < 0
            or self.know < 0
        ):
            raise ValidationError('Progress values ​​cannot be negative')

    def save(self, *args: object, **kwargs: object) -> None:
        """Call clean() before saving."""
        self.full_clean()
        super().save(*args, **kwargs)  # type: ignore[arg-type]
