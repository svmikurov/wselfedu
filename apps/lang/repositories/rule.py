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
            'question_translation__foreign',
            'answer_translation__foreign',
        )
        children_qs = models.RuleClause.objects.all()
        clauses_qs = models.RuleClause.objects.select_related(
            'parent'
        ).prefetch_related(
            Prefetch('examples', queryset=examples_qs),
            Prefetch('children', queryset=children_qs),
        )

        exceptions_qs = models.RuleException.objects.select_related(
            'question_translation__foreign',
            'answer_translation__foreign',
        )

        return models.Rule.objects.prefetch_related(
            Prefetch('clauses', queryset=clauses_qs),
            Prefetch('exceptions', queryset=exceptions_qs),
        ).get(pk=rule_id, user=user)
