"""Language rule repository."""

from django.db.models import Prefetch

from apps.lang import models
from apps.users.models import Person

from .abc import RuleRepositoryABC


class RuleRepository(RuleRepositoryABC):
    """Language rule repository."""

    @classmethod
    def get_for_user(cls, user: Person, rule_id: int) -> models.Rule:
        """Get rule with all examples and exceptions."""
        return cls._fetch(user, rule_id)

    @staticmethod
    def _fetch(user: Person, rule_id: int) -> models.Rule:
        """Get rule queryset with clauses, examples and exceptions."""
        examples_qs = models.RuleExample.objects.select_related(
            'question_translation__english',
            'answer_translation__english',
        )
        return models.Rule.objects.prefetch_related(
            Prefetch(
                'clauses',
                queryset=models.RuleClause.objects.prefetch_related(
                    Prefetch('examples', queryset=examples_qs)
                ),
            ),
            Prefetch(
                'exceptions',
                queryset=models.RuleException.objects.select_related(
                    'question_translation__english',
                    'answer_translation__english',
                ),
            ),
        ).get(pk=rule_id, user=user)
