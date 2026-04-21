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

from apps.core.adapters.exercise.process import (
    ExerciseProcessAdapter,
)
from apps.core.builders.exercise import (
    ExerciseCaseBuilder,
    ExercisePresentationBuilder,
)
from apps.core.domains.exercise import PresentationDomain
from apps.core.domains.exercise.deps.selector import (
    CandidatesSelector,
)
from apps.core.domains.exercise.dto import (
    ExerciseParametersDTO,
    TestExerciseConfigDTO,
)
from apps.core.domains.exercise.enums import (
    ExerciseProcessEnum,
    ExerciseStatusEnum,
    ExerciseTypeEnum,
)
from apps.core.resolvers.exercise.config_resolver import (
    ExerciseConfigurationResolver,
)
from apps.core.services.exercise.generic import (
    CreateExerciseService,
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
            ExerciseProcessEnum.CREATE_CASE: Factory(
                ExerciseProcessAdapter,
            )
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
                builder=Factory(
                    ExerciseCaseBuilder,
                ),
            ),
        },
    )
    regular_translation_presentation_builder_registry = Dict(
        {
            ExerciseStatusEnum.NEW_TASK: Factory(
                ExercisePresentationBuilder,
            ),
        },
    )

    process_regular_translation_presentation = Factory(
        ExerciseUseCaseStrategy,
        prefix='regular_translation_presentation',
        storage=user_command_storage,
        config_resolver=configurations.exercise_config_resolver,
        adapter_registry=regular_translation_presentation_adapter_registry,
        service_registry=regular_translation_presentation_service_registry,
        builder_registry=regular_translation_presentation_builder_registry,
    )

    # =============================================
    # Regular translation test
    # =============================================
    # ---------------------------------------------
    # Regular translation test dependencies
    # ---------------------------------------------
    # QUESTION: Is deprecated?
    regular_translation_test_config_resolver = Factory(
        ExerciseConfigurationResolver,
        exercise_type=ExerciseTypeEnum.TEST,
        parameters_repository=repositories.translation_parameters,
        default=ExerciseParametersDTO(
            settings=TestExerciseConfigDTO(
                option_count=7,
            ),
        ),
    )
