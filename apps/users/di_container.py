"""Defines DI container for Users app."""

from dependency_injector import containers, providers

from .presenters import (
    MentorshipPresenter,
    StudentExercisesPresenter,
)
from .services.mentorship import (
    MentorshipService,
)


class UsersContainer(containers.DeclarativeContainer):
    """DI container for Users app."""

    mentorship_service = providers.Factory(
        MentorshipService,
    )
    mentorship_presenter = providers.Factory(
        MentorshipPresenter,
    )

    exercises_presenter = providers.Factory(
        StudentExercisesPresenter,
    )
