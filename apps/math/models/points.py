"""Defines Mathematical application reward history."""

from django.db import models

from apps.math.models.simple import SimpleTask


class SimplCalcReward(models.Model):
    """Simple calculation task reward history."""

    task = models.ForeignKey(
        SimpleTask,
        on_delete=models.CASCADE,
    )
    reward = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        """Configure the model."""

        db_table = 'math_simpl_calc_reward'
