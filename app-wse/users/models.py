from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy


class UserModel(AbstractUser, models.Model):
    """Simple user model.

    Contain only name, password and update date user data.
    """

    updated_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """Represent an instance as a string."""
        return self.username

    def get_absolute_url(self):
        """Return the url of an instance."""
        return reverse_lazy('users:detail', kwargs={'pk': self.pk})
