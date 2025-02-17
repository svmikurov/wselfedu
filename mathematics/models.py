"""Mathematics tasks."""

from django.db import models

from config.constants import CALCULATION_TYPES
from users.models import UserApp
from users.models.points import Transaction


class MathematicsTasks(models.Model):
    """Mathematics tasks."""

    user = models.ForeignKey(UserApp, on_delete=models.CASCADE)
    exercise = models.CharField(
        choices=CALCULATION_TYPES,
        max_length=10,
    )
    operand1 = models.SmallIntegerField()
    operand2 = models.SmallIntegerField()
    answer = models.SmallIntegerField()
    is_correctly = models.BooleanField(blank=True, null=True)
    time = models.PositiveSmallIntegerField(blank=True, null=True)
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Начисление очков',
        related_name='math',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model features."""

        verbose_name = 'Решение задания пользователем'
        verbose_name_plural = 'Решения заданий пользователем'
