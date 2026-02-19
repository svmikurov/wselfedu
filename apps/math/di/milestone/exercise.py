"""User's and student's exercise perform milestone."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.math.milestones import calculation, service


# NOTE: It's experimental milestone definition
class ExerciseMilestoneContainer(DeclarativeContainer):
    """User's and student's exercise perform milestone."""

    progress_service = Factory(
        service.CalculationProgressService,
    )
    reward_service = Factory(
        service.CalculationRewardService,
    )

    user_calculation = Factory(
        calculation.UserCalculationMilestone,
        progress_service=progress_service,
    )
    student_calculation = Factory(
        calculation.StudentCalculationMilestone,
        progress_service=progress_service,
        reward_service=reward_service,
    )
