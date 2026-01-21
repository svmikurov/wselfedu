"""Defines lang app exercise model."""

from django.db import models

from apps.core.models.base import BaseExercise


class LangExercise(BaseExercise):
    """Lang app exercise model."""

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Создавший упражнение',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'

        unique_together = ['name', 'user']

        db_table = 'lang_exercise'
