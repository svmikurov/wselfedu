"""User's and student's exercise perform milestone."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Factory

from apps.math.milestones import calculation, service
from apps.math.models import StudentCalculationCondition
from apps.math.services import completion


class MilestoneContainer(DeclarativeContainer):
    """User's and student's exercise perform milestone."""

    # ===========================================
    # External dependencies
    # -------------------------------------------
    reward_service = Dependency()  # type: ignore[var-annotated]

    # ===========================================
    # Internal dependencies
    # -------------------------------------------
    calculation_progress_service = Factory(
        service.CalculationProgressService,
    )
    student_calculation_completion_service = Factory(
        completion.CalculationCompletionService,
        manager=StudentCalculationCondition.objects,
    )

    # ===========================================
    # User's milestones
    # -------------------------------------------
    user_calculation = Factory(
        calculation.UserCalculationMilestone,
        progress_service=calculation_progress_service,
    )

    # ===========================================
    # Student's milestones
    # -------------------------------------------
    student_calculation = Factory(
        calculation.StudentCalculationMilestone,
        reward_service=reward_service,
        completion_service=student_calculation_completion_service,
        exercise_manager=StudentCalculationCondition.objects,
    )
