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

from apps.core.adapters.exercise import (
    ExerciseProcessAdapter,
    ExerciseProgressAdapter,
)
from apps.core.builders.exercise.task import (
    ExercisePresentationBuilder,
    TestExerciseTaskBuilder,
)
from apps.core.resolvers.exercise.config_resolver import (
    ExerciseConfigurationResolver,
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

    services = DependenciesContainer()
    repositories = DependenciesContainer()
    lang_config = DependenciesContainer()

    user_command_storage = Dependency()  # type: ignore[var-annotated]
    auditor = Dependency()  # type: ignore[var-annotated]

    # =============================================
    # Regular translation presentation exercise
    # =============================================

    regular_translation_presentation_adapter_registry = Dict(
        {
            ExerciseAction.CREATE_TASK: Factory(
                ExerciseProcessAdapter, name='Process exercise command adapter'
            ),
            ExerciseAction.UPDATE_PROGRESS: Factory(
                ExerciseProgressAdapter,
                name='Progress exercise command adapter',
            ),
        },
    )
    regular_translation_presentation_builder_registry = Dict(
        {
            ExerciseStatus.NEW_TASK: Factory(ExercisePresentationBuilder),
        },
    )

    regular_translation_presentation = Factory(
        ExerciseUseCaseStrategy,
        prefix='regular_translation_presentation',
        storage=user_command_storage,
        config_resolver=lang_config.translation_exercise_config_resolver,
        adapter_registry=regular_translation_presentation_adapter_registry,
        service_registry=services.regular_translation_presentation_registry,
        builder_registry=regular_translation_presentation_builder_registry,
        auditor=auditor,
        name='Exercise use case strategy',
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
        service_registry=services.regular_translation_test_registry,
        builder_registry=regular_translation_test_builder_registry,
        auditor=auditor,
        name='Regular translation test',
    )
