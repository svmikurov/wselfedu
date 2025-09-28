"""Defines lang app exercise model."""

from apps.core.models.base import BaseExercise


class LangExercise(BaseExercise):
    """Lang app exercise model."""

    class Meta:
        """Model configuration."""

        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
        db_table = 'lang_exercise'
