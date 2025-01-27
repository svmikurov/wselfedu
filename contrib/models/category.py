"""Item category base model."""

from django.db import models

from users.models import UserApp


class Category(models.Model):
    """Item category base model."""

    name = models.CharField(
        max_length=30,
        verbose_name='Наименование категории',
        help_text='Не более 30 символов.',
    )
    user = models.ForeignKey(
        UserApp,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Set up the model."""

        abstract = True
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self) -> str:
        """Provide the informal string representation of an object."""
        return self.name
