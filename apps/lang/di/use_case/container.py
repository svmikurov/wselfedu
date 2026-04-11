"""Language discipline use case DI container."""

from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Dict,
    Factory,
)

from apps.core.domains.exercise import (
    PresentationDomain,
)
from apps.core.domains.exercise.deps.selector import (
    CandidatesSelector,
)
from apps.core.domains.exercise.dto import (
    ExerciseParametersDTO,
    TestExerciseConfigDTO,
)
from apps.core.domains.exercise.enums import (
    ExerciseProcessEnum,
    ExerciseTypeEnum,
)
from apps.core.services.exercise.generic import (
    CreateExerciseService,
)
from apps.core.use_cases.exercise.config_resolver import (
    ExerciseConfigurationResolver,
)
from apps.core.use_cases.exercise.generic import (
    ExerciseUseCaseStrategy,
)


class UseCaseContainer(DeclarativeContainer):
    """Language discipline use case DI container."""

    # =============================================
    # External dependencies
    # =============================================
    repositories = DependenciesContainer()
    configurations = DependenciesContainer()

    user_command_storage = Dependency()  # type: ignore[var-annotated]

    # =============================================
    # Regular translation presentation
    # =============================================
    regular_translation_presentation_adapter_registry = Dict(
        {
            ExerciseProcessEnum.CREATE_CASE: ...,
        },
    )
    regular_translation_presentation_service_registry = Dict(
        {
            ExerciseProcessEnum.CREATE_CASE: Factory(
                CreateExerciseService,
                candidates_repository=repositories.translation_candidates,
                domain=Factory(
                    PresentationDomain,
                    selector=Factory(CandidatesSelector),
                ),
            ),
        },
    )
    regular_translation_presentation_factory_registry = Dict(
        {
            ExerciseProcessEnum.CREATE_CASE: ...,
        },
    )
    process_regular_translation_presentation = Factory(
        ExerciseUseCaseStrategy,
        store_prefix='regular_translation_presentation',
        storage=user_command_storage,
        config_resolver=configurations.exercise_config_resolver,
        adapter_registry=regular_translation_presentation_adapter_registry,
        service_registry=regular_translation_presentation_service_registry,
        factory_registry=regular_translation_presentation_factory_registry,
    )

    # =============================================
    # Regular translation test
    # =============================================
    # ---------------------------------------------
    # Regular translation test dependencies
    # ---------------------------------------------
    regular_translation_test_config_resolver = Factory(
        ExerciseConfigurationResolver,
        exercise_type=ExerciseTypeEnum.TEST,
        parameters_repository=repositories.translation_parameters,
        default=ExerciseParametersDTO(
            conf=TestExerciseConfigDTO(
                option_count=7,
            ),
        ),
    )
