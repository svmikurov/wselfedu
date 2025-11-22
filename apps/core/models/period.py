"""Education data source."""

from django.db import models


class Period(models.Model):
    """Period add education data."""

    name = models.CharField(
        max_length=40,
        verbose_name='Период',
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

        verbose_name = 'Период'
        verbose_name_plural = 'Периоды'

    def __str__(self) -> str:
        """Get the string representation of period."""
        return str(self.name)
