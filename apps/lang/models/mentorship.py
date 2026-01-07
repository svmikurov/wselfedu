"""English language rule to study via mentorship."""

from django.db import models


class MentorshipEnglishRule(models.Model):
    """English rule study via mentorship."""

    mentorship = models.ForeignKey(
        'users.Mentorship',
        on_delete=models.CASCADE,
        related_name='english_rules',
        verbose_name='Наставничество',
        help_text='Наставничество для изучения правила',
    )
    rule = models.ForeignKey(
        'Rule',
        on_delete=models.CASCADE,
        related_name='mentorships',
        verbose_name='Правило для изучения',
        help_text='Правило для изучения в наставничестве',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата добавления',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата изменения',
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
