"""English language rule to study via mentorship model."""

from django.db import models

from apps.core.models import AbstractBaseModel

__all__ = [
    'MentorshipEnglishRule',
]


class MentorshipEnglishRule(AbstractBaseModel):
    """English rule study via mentorship."""

    mentorship = models.ForeignKey(
        'users.Mentorship',
        on_delete=models.CASCADE,
        related_name='english_rules',
        verbose_name='Наставничество',
        help_text='Наставничество для изучения правила',
    )
    rule = models.ForeignKey(
        'lang.Rule',
        on_delete=models.CASCADE,
        related_name='mentorships',
        verbose_name='Правило для изучения',
        help_text='Правило для изучения в наставничестве',
    )

    class Meta:
        """Model configuration."""

        verbose_name = (
            'Правило английского языка для изучения в наставничестве'
        )
        verbose_name_plural = (
            'Правила английского языка для изучения в наставничестве'
        )

        ordering = ['mentorship', 'created_at']

        unique_together = ['mentorship', 'rule']

        db_table = 'lang_english_mentorship_rule'
