"""Assigned exercise."""

from django.db import models


class EnglishAssignedExercise(models.Model):
    """Assigned English exercise."""

    mentorship = models.ForeignKey(
        'users.Mentorship',
        on_delete=models.CASCADE,
        verbose_name='Наставничество',
    )
    exercise = models.ForeignKey(
        'LangExercise',
        on_delete=models.CASCADE,
        verbose_name='Упражнение',
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

        verbose_name = 'Назначенное упражнение по английскому'
        verbose_name_plural = 'Назначенные упражнения по английскому'

        db_table = 'lang_assigned_english_exercise'
