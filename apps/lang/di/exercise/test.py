"""DI container for translation study via Test exercises."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Configuration,
    Container,
    Dependency,
    Factory,
)

from apps.lang import use_cases

from ._service import ExerciseServiceContainer
from ._validator import TranslationValidatorContainer

if TYPE_CHECKING:
    from apps.core.storage.services import TaskStorage
    from apps.lang.use_cases import types

    type StorageFactory = Factory[TaskStorage[Any]]

    type WebRegularFactory = Factory[types.WebTest]
    type WebAssignedFactory = Factory[types.WebAssignedTest]
    type WebProgressFactory = Factory[Any]


class TranslationTestContainer(DeclarativeContainer):
    """DI container for translation test exercises."""

    # ---------------------
    # External dependencies
    # ---------------------

    task_storage: Dependency[StorageFactory] = Dependency()
    web_adapter = Dependency()  # type: ignore[var-annotated]

    # ---------------------------
    # Test exercise configuration
    # ---------------------------

    config = Configuration()
    config.from_dict(
        {
            'option_count': 5,
            'limit': 100,
            'case_storage_ttl': 600,
        }
    )

    # -------------------
    # External Containers
    # -------------------

    validators = Container(TranslationValidatorContainer)
    services = Container(
        ExerciseServiceContainer,
        case_storage=task_storage,
        exercise_config=config,
    )

    # --------
    # UseCases
    # --------

    web_regular_use_case: WebRegularFactory = Factory(
        use_cases.UseCase,
        validator=validators.web_regular_validator,
        service=services.user_translation_service,
        response_adapter=web_adapter,
    )
    web_assigned_use_case: WebAssignedFactory = Factory(
        use_cases.DetailUseCase,
        validator=validators.web_assigned_validator,
        service=services.assigned_service,
        response_adapter=web_adapter,
    )

    # Translation study have study progress tracking.
    web_progress_use_case: WebProgressFactory = Factory(
        use_cases.UseCase,
        validator=validators.web_regular_validator,
        service=services.progress_service,
        response_adapter=web_adapter,
    )
