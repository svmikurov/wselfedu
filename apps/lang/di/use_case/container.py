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
from apps.core.builders.exercise.case import ExerciseCaseBuilder
from apps.core.builders.exercise.task import (
    ExercisePresentationBuilder,
    TestExerciseTaskBuilder,
)
from apps.core.domains.exercise import PresentationDomain, TestDomain
from apps.core.domains.exercise.deps.selector import (
    CandidatesSelector,
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
from contracts.enums.exercise import (
    ExerciseAction,
    ExerciseKind,
    ExerciseStatus,
)
from contracts.schemas.domain.exercise.params import (
    ExerciseParametersDTO,
    TestExerciseConfigDTO,
)


class UseCaseContainer(DeclarativeContainer):
    """Language discipline use case DI container."""

    # =============================================
    # External dependencies
    # =============================================

    repositories = DependenciesContainer()
    configurations = DependenciesContainer()

    user_command_storage = Dependency()  # type: ignore[var-annotated]
    auditor = Dependency()  # type: ignore[var-annotated]

    # =============================================
    # Regular translation presentation exercise
    # =============================================

    regular_translation_presentation_adapter_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: Factory(ExerciseProcessAdapter),
        },
    )
    regular_translation_presentation_service_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: Factory(
                CreateExerciseService,
                candidates_repository=repositories.translation_candidates,
                domain=Factory(
                    PresentationDomain,
                    selector=Factory(CandidatesSelector),
                ),
                builder=Factory(ExerciseCaseBuilder),
            ),
        },
    )
    regular_translation_presentation_builder_registry = Dict(
        {
            ExerciseStatus.NEW_TASK: Factory(ExercisePresentationBuilder),
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
        auditor=auditor,
    )

    # =============================================
    # Regular translation test exercise
    # =============================================

    regular_translation_test_config_resolver = Factory(
        ExerciseConfigurationResolver,
        exercise_type=ExerciseKind.TEST,
        parameters_repository=repositories.translation_parameters,
        default=ExerciseParametersDTO(
            settings=TestExerciseConfigDTO(
                option_count=7,
            ),
        ),
    )

    regular_translation_test_adapter_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: Factory(ExerciseProcessAdapter),
        },
    )
    regular_translation_test_service_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: Factory(
                CreateExerciseService,
                candidates_repository=repositories.translation_candidates,
                domain=Factory(
                    TestDomain,
                    selector=Factory(CandidatesSelector),
                ),
                builder=Factory(ExerciseCaseBuilder),
            ),
        },
    )
    regular_translation_test_builder_registry = Dict(
        {
            ExerciseStatus.NEW_TASK: Factory(TestExerciseTaskBuilder),
        },
    )

    process_regular_translation_test = Factory(
        ExerciseUseCaseStrategy,
        prefix='regular_translation_test',
        storage=user_command_storage,
        config_resolver=regular_translation_test_config_resolver,
        adapter_registry=regular_translation_test_adapter_registry,
        service_registry=regular_translation_test_service_registry,
        builder_registry=regular_translation_test_builder_registry,
        auditor=auditor,
    )
