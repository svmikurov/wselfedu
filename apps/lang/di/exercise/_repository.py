"""DI container for translation study Repository."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory

from apps.lang.repositories import (
    ExerciseTranslationRepository,
    UserTranslationRepository,
)


class TranslationRepositoryContainer(DeclarativeContainer):
    """DI container for translation study Repository."""

    exercise_translation_repository = Factory(
        ExerciseTranslationRepository,
    )
    user_translation_repository = Factory(
        UserTranslationRepository,
    )
