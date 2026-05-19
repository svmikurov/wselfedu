"""Item study lookup conditions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final, Self

from django.db import models

from apps.core.models import AbstractBaseModel
from ports.interfaces.request_data.api.general import IdName

if TYPE_CHECKING:
    from apps.users.models import Person
    from ports.refactor.lang import types

__all__ = ('ExerciseConditions',)


class ExerciseConditions(AbstractBaseModel):
    """Item study lookup conditions for exercise."""

    DEFAULTS: Final[dict[types.Progress, bool]] = {
        'is_study': True,
        'is_repeat': True,
        'is_examine': True,
        'is_know': False,
    }

    user = models.ForeignKey(
        'users.Person',
        on_delete=models.CASCADE,
        verbose_name='User',
        related_name='user_conditions',
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Category',
        related_name='category_conditions',
    )
    mark = models.ForeignKey(
        'Mark',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Mark',
        related_name='mark_conditions',
    )
    word_source = models.ForeignKey(
        'core.Source',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Source',
    )

    # Word adding period
    start_period = models.ForeignKey(
        'core.Period',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Start period',
        related_name='start_periods',
        help_text='Added after data',
    )
    end_period = models.ForeignKey(
        'core.Period',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='End period',
        related_name='end_periods',
        help_text='Added before data',
    )

    # Study progress
    progress_bar = models.ForeignKey(
        'study.ProgressBar',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Progress bar version',
    )
    is_study = models.BooleanField(
        blank=True,
        null=True,
        default=DEFAULTS['is_study'],
        verbose_name='Study',
        help_text='Selected words for study',
    )
    is_repeat = models.BooleanField(
        blank=True,
        null=True,
        default=DEFAULTS['is_repeat'],
        verbose_name='Repeat',
        help_text='Selected words for repetition',
    )
    is_examine = models.BooleanField(
        blank=True,
        null=True,
        default=DEFAULTS['is_examine'],
        verbose_name='Examine',
        help_text='Select words to examine',
    )
    is_know = models.BooleanField(
        blank=True,
        null=True,
        default=DEFAULTS['is_know'],
        verbose_name='Know',
        help_text='Select the learned words',
    )

    class Meta:
        """Model configuration."""

        verbose_name = 'Word learning conditions'
        verbose_name_plural = 'Word learning conditions'

        # TODO: Add constrains after Period model improve
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                name='lang_exercise_configuration_unique_user_name',
            ),
        ]

        db_table = 'lang_exercise_configuration'

    def obj_to_id_name(self, field: types.Option) -> IdName | None:
        """Convert object to {id, name} dict."""
        obj = getattr(self, field, None)
        if obj and hasattr(obj, 'id') and hasattr(obj, 'name') and obj.id:
            return {'id': obj.id, 'name': obj.name}
        return None

    def get_progress(self, field: types.Progress) -> bool:
        """Get progress user value if it set or return default."""
        # Check if an attribute exists (for an empty instance)
        attr = getattr(self, field, None)
        return attr if attr is not None else self.DEFAULTS[field]

    @property
    def study(self) -> bool:
        """Is study."""
        return self.get_progress('is_study')

    @property
    def repeat(self) -> bool:
        """Is repeat."""
        return self.get_progress('is_repeat')

    @property
    def examine(self) -> bool:
        """Is examine."""
        return self.get_progress('is_examine')

    @property
    def know(self) -> bool:
        """Is know."""
        return self.get_progress('is_know')

    @classmethod
    def get_instants(cls, user: Person) -> Self:
        """Get user translation conditions or return defaults."""
        try:
            return cls.objects.get(user=user)
        except cls.DoesNotExist:
            return cls()
