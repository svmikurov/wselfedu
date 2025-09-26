"""Defines student study models."""

from typing import Any

from django.db import models

from apps.core.models.base import BaseExercise
from apps.core.models.exercise import Exercise
from apps.users.models import Mentorship

BASE_EXERCISE = BaseExercise


def get_subclasses_choices() -> dict[str, Any]:
    """Get exercise models for choice."""
    return {
        'model__in': [
            m._meta.model_name for m in BASE_EXERCISE.__subclasses__()
        ]
    }


class ExerciseAssigned(models.Model):
    """Assigned exercise to student by mentor the model."""

    mentorship = models.ForeignKey(
        Mentorship,
        on_delete=models.CASCADE,
        related_name='exercises',
        verbose_name='Наставничество',
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name='assigned_exercise',
        verbose_name='Назначенное упражнение',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата назначения',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        db_table = 'study_assigned'
        indexes = [models.Index(fields=['mentorship', 'exercise'])]

    def __str__(self) -> str:
        """Get the string representation of model instance."""
        return str(self.exercise)


class ExerciseActive(models.Model):
    """Active exercises."""

    class IsActive(models.IntegerChoices):
        """Activation action choice."""

        ACTIVATED = (1, 'Активировано')
        DEACTIVATED = (0, 'Деактивировано')

    exercise = models.ForeignKey(
        'ExerciseAssigned',
        on_delete=models.CASCADE,
        verbose_name='Назначенное упражнение',
        related_name='activation_status',
    )
    is_active = models.BooleanField(
        choices=IsActive.choices,
        default=IsActive.DEACTIVATED,
        verbose_name='Статус активации',
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

        verbose_name = 'Статус активации упражнения'
        verbose_name_plural = 'Статусы активации упражнения'
        db_table = 'study_assigned_active'


class ExerciseExpiration(models.Model):
    """Expiry date of the exercise execution."""

    exercise = models.ForeignKey(
        'ExerciseAssigned',
        on_delete=models.CASCADE,
        verbose_name='Назначенное упражнение',
        related_name='exercise_expiration',
    )
    is_daily = models.BooleanField(
        default=False,
        verbose_name='Ежедневное задание',
    )
    expiration = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Срок действия задания',
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

        verbose_name = 'Срок выполнения упражнения'
        verbose_name_plural = 'Сроки выполнения упражнения'
        db_table = 'study_assigned_expiration'


class ExerciseTaskCount(models.Model):
    """Exercise task count."""

    exercise = models.ForeignKey(
        'ExerciseAssigned',
        on_delete=models.CASCADE,
        verbose_name='Количество назначенных заданий',
        related_name='exercise_task_count',
    )
    count = models.PositiveSmallIntegerField()
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

        verbose_name = 'Количество назначенных заданий'
        verbose_name_plural = 'Количества назначенных заданий'
        db_table = 'study_assigned_task_count'


class ExerciseTaskAward(models.Model):
    """Exercise task award."""

    exercise = models.ForeignKey(
        ExerciseAssigned,
        on_delete=models.CASCADE,
        verbose_name='Упражнение',
        related_name='task_award',
    )
    award = models.PositiveSmallIntegerField(
        verbose_name='Вознаграждение',
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

        verbose_name = 'Вознаграждение за задание'
        verbose_name_plural = 'Вознаграждения за задание'
        db_table = 'study_assigned_task_award'


class AssignationCompletes(models.Model):
    """Model of completed assigned tasks."""

    assignation = models.ForeignKey(
        ExerciseAssigned,
        on_delete=models.CASCADE,
        related_name='exercise_completion',
        verbose_name='Назначенное упражнение',
    )
    attempt_count = models.PositiveSmallIntegerField(
        verbose_name='Кол-во попыток',
    )
    success_count = models.PositiveSmallIntegerField(
        verbose_name='Кол-во успешных решений',
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

        verbose_name = 'Выполнение назначенного задания'
        verbose_name_plural = 'Выполнения назначенного задания'
        db_table = 'study_assigned_completion'
