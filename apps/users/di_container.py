"""Defines Users app DI container."""

from dependency_injector import containers, providers

from .presenters import (
    MentorshipPresenter,
    StudentExercisesPresenter,
)
from .services import AwardService, MentorshipService, RewardService


class UsersContainer(containers.DeclarativeContainer):
    """DI container for Users app dependencies."""

    mentorship_service = providers.Factory(
        MentorshipService,
    )
    mentorship_presenter = providers.Factory(
        MentorshipPresenter,
    )

    exercises_presenter = providers.Factory(
        StudentExercisesPresenter,
    )

    # DEPRECATED: `AwardService` will be deleted
    award_service = providers.Factory(
        AwardService,
    )
    reward_service = providers.Factory(
        RewardService,
    )
