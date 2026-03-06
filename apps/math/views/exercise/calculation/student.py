"""Student's calculation exercises."""

from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    CharField,
    IntegerField,
    OuterRef,
    QuerySet,
    Subquery,
)
from django.views.generic import ListView

from apps.core.views import UserLoginRequiredMixin
from apps.math.models import StudentCalculationCondition
from apps.study.models import ExerciseAvailability, ExerciseReward


class StudentCalculationExerciseListVew(
    UserLoginRequiredMixin,
    ListView,  # type: ignore
):
    """Student's calculation exercises."""

    template_name = 'math/exercise/calculation/student/index.html'
    model = StudentCalculationCondition
    context_object_name = 'exercises'

    def get_queryset(self) -> QuerySet[StudentCalculationCondition]:
        """Return mentor's assignations for students."""
        content_type = ContentType.objects.get_for_model(
            StudentCalculationCondition
        )

        reward_subquery = ExerciseReward.objects.filter(
            exercise_content_type=content_type,
            exercise_object_id=OuterRef('pk'),
        ).values('amount', 'reward_type')[:1]
        availability_subquery = ExerciseAvailability.objects.filter(
            exercise_content_type=content_type,
            exercise_object_id=OuterRef('pk'),
        ).values('required_count', 'period_type')[:1]

        exercises = (
            StudentCalculationCondition.objects.filter(
                mentorship__student=self.user
            )
            .select_related(
                'mentorship__student',
                'mentorship__mentor',
                'calculation_condition',
            )
            .annotate(
                reward_amount=Subquery(
                    reward_subquery.values('amount')[:1],
                    output_field=IntegerField(),
                ),
                reward_type=Subquery(
                    reward_subquery.values('reward_type')[:1],
                    output_field=CharField(),
                ),
                availability_count=Subquery(
                    availability_subquery.values('required_count')[:1],
                    output_field=IntegerField(),
                ),
                availability_period=Subquery(
                    availability_subquery.values('period_type')[:1],
                    output_field=CharField(),
                ),
                is_completed=Subquery(
                    availability_subquery.values('is_completed')[:1],
                ),
                is_active=Subquery(
                    availability_subquery.values('is_active')[:1],
                ),
            )
        ).order_by('created_at')

        return exercises
