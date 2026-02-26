"""Users application DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.users import presenters, services


class UsersContainer(DeclarativeContainer):
    """Users application DI container."""

    # ===========================================
    # Internal services
    # -------------------------------------------
    mentorship_service = Factory(
        services.MentorshipService,
    )

    reward_service = Factory(
        services.RewardService,
    )
    # DEPRECATED: Award service
    award_service = Factory(
        services.AwardService,
    )

    # ===========================================
    # Presenters
    # -------------------------------------------
    mentorship_presenter = Factory(
        presenters.MentorshipPresenter,
    )

    exercises_presenter = Factory(
        presenters.StudentExercisesPresenter,
    )
