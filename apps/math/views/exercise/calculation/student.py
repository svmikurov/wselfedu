"""Student's calculation exercises."""

from django.db.models import QuerySet
from django.views.generic import ListView

from apps.core.views import UserLoginRequiredMixin
from apps.math.models import StudentCalculationCondition


class AssignedCalculationExerciseStudentListVew(
    UserLoginRequiredMixin,
    ListView,  # type: ignore
):
    """Student's calculation exercises."""

    template_name = 'math/exercise/calculation/student/index.html'
    model = StudentCalculationCondition
    context_object_name = 'exercises'

    def get_queryset(self) -> QuerySet[StudentCalculationCondition]:
        """Get student's assigned calculations."""
        return (
            super()
            .get_queryset()
            .filter(
                mentorship__student=self.user,
            )
            .select_related(
                'mentorship__mentor',
                'calculation_condition',
            )
        )
