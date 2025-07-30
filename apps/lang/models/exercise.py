"""Defines lang app exercise model."""

from apps.core.models import BaseExercise


class LangExercise(BaseExercise):
    """Lang app exercise model."""

    class Meta:
        """Model configuration."""

        managed = False
        db_table = 'lang"."exercise'
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'
