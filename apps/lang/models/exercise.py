"""Defines lang app exercise model."""

from apps.main.models import BaseExercise


class LangExercise(BaseExercise):
    """Lang app exercise model."""

    class Meta:
        """Model configuration."""

        managed = False
        db_table = 'lang"."exercise'
