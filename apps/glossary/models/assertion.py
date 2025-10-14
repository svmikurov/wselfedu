"""Assertion for a specific term."""

from django.db import models


class TermAssertion(models.Model):
    """Term assertion model."""

    term = models.ForeignKey(
        'Term',
        on_delete=models.CASCADE,
        related_name='assertions',
        verbose_name='Термин',
    )
    assertion = models.CharField(
        max_length=255,
        verbose_name='Утверждение',
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
        """Configure the model."""

        verbose_name = 'Утверждение о термине'
        verbose_name_plural = 'Утверждения о термине'
        ordering = ['-created_at']
