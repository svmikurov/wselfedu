"""DI container for translation study Service."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, Dependency, Factory

from apps.lang.domain import AssignedTestTranslationDomain
from apps.lang.repositories import ExerciseTranslationRepository
from apps.lang.services import (
    AssignedTestService,
    TestProgressService,
    UserTestService,
)

from ._repository import TranslationRepositoryContainer

if TYPE_CHECKING:
    # External dependencies
    type StorageDependency = Dependency[Any]
    type ConfigDependency = Dependency[Any]

    # Container dependencies
    type RepositoryFactory = Factory[ExerciseTranslationRepository]

    type DomainFactory = Factory[AssignedTestTranslationDomain]

    type AssignedServiceFactory = Factory[AssignedTestService]
    type UserServiceFactory = Factory[UserTestService]
    type ProgressServiceFactory = Factory[TestProgressService]


class ExerciseServiceContainer(DeclarativeContainer):
    """DI container for translation study Service."""

    # -------------------
    # External containers
    # -------------------

    repository_container = Container(
        TranslationRepositoryContainer,
    )

    # ---------------------
    # External Dependencies
    # ---------------------

    case_storage: StorageDependency = Dependency()
    exercise_config: ConfigDependency = Dependency()

    # -----------------
    # Exercise Domain
    # -----------------

    domain: DomainFactory = Factory(
        AssignedTestTranslationDomain,
    )

    # -----------------
    # Exercise Services
    # -----------------

    user_translation_service: UserServiceFactory = Factory(
        UserTestService,
        repository=repository_container.user_translation_repository,
        storage=case_storage,
        config=exercise_config,
        domain=domain,
    )

    progress_service: ProgressServiceFactory = Factory(
        TestProgressService,
        repository=repository_container.user_translation_repository,
        storage=case_storage,
        config=exercise_config,
        domain=domain,
    )

    assigned_service: AssignedServiceFactory = Factory(
        AssignedTestService,
        repository=repository_container.exercise_translation_repository,
        storage=case_storage,
        config=exercise_config,
        domain=domain,
    )
