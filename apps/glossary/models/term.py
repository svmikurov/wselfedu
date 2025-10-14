"""Term model."""

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy


class Term(models.Model):
    """Term model."""

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='user_terms',
        verbose_name='Пользователь',
    )
    name = models.CharField(
        max_length=50,
        verbose_name='Термин',
    )
    definition = models.CharField(
        max_length=250,
        verbose_name='Определение',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлен',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Изменен',
    )

    class Meta:
        """Configure the model."""

        verbose_name = 'Термин'
        verbose_name_plural = 'Термины'
        ordering = ['-created_at']

    def get_absolute_url(self) -> str:
        """Get object url path."""
        url: str = reverse_lazy('glossary:term_detail', kwargs={'pk': self.pk})
        return url

    def __str__(self) -> str:
        """Get string representation of term instance."""
        return str(self.name)
