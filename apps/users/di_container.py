"""Defines Users app DI container."""

from dependency_injector import containers, providers

from .presenters import (
    MentorshipPresenter,
    StudentExercisesPresenter,
)
from .services.mentorship import (
    MentorshipService,
)


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
