"""Word study configuration model."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from django.db import models

from apps.core.models import AbstractBaseModel

if TYPE_CHECKING:
    from apps.users.models import Person

__all__ = ('TranslationConfiguration',)


class TranslationConfiguration(AbstractBaseModel):
    """Translation study configuration model."""

    class TranslateChoices(models.TextChoices):
        """Translate order choices."""

        FROM_NATIVE = 'from_native', 'С родного языка'
        TO_NATIVE = 'to_native', 'На родной язык'
        RANDOM = 'random', 'Случайный порядок'

    DEFAULT_TRANSLATION_ORDER = TranslateChoices.TO_NATIVE

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_translation_settings',
    )

    display_order = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=TranslateChoices.choices,
        default=DEFAULT_TRANSLATION_ORDER,
        verbose_name='Порядок перевода',
    )
    word_count = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Максимальное количество слов',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Настройки изучения переводов'
        verbose_name_plural = 'Настройки изучения переводов'

        db_table = 'lang_translation_configuration'

        # TODO: Add constrains after Period model improve
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='lang_translation_configuration_unique_user_name',
            ),
        ]

    # @property
    # def translation_order_display(self) -> str:
    #     """Get a human-readable translation name."""
    #     return self.get_translation_order_display()

    @classmethod
    def resolve_order_choice(
        cls, order_value: str | None = None
    ) -> tuple[str, str]:
        """Resolve order choice, return default if None."""
        choice = (
            cls.TranslateChoices(order_value)
            if order_value
            else cls.TranslateChoices.TO_NATIVE
        )
        return choice.value, choice.label

    @classmethod
    def get_instants(cls, user: Person) -> Self:
        """Get user translation configuration or return defaults."""
        try:
            instance = cls.objects.get(user=user)
        except cls.DoesNotExist:
            return cls()
        return instance
