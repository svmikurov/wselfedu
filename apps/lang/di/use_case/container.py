"""Language discipline use case DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Factory,
)

from apps.core.use_cases.exercise.generic import ExerciseUseCaseStrategy


class LangUseCaseContainer(DeclarativeContainer):
    """Language discipline use case DI container."""

    # =============================================
    # External dependencies
    # =============================================

    lang_config = DependenciesContainer()
    spec_factories = DependenciesContainer()
    services = DependenciesContainer()
    use_case_result_builders = DependenciesContainer()

    user_command_storage = Dependency()  # type: ignore[var-annotated]
    auditor = Dependency()  # type: ignore[var-annotated]

    # =============================================
    # Regular exercises
    # =============================================

    regular_translation_presentation = Factory(
        ExerciseUseCaseStrategy,
        prefix='regular_translation_presentation',
        storage=user_command_storage,
        config_resolver=lang_config.translation_presentation_resolver,
        spec_factory_registry=spec_factories.presentation_registry,
        service_registry=services.regular_translation_presentation_registry,
        builder_registry=use_case_result_builders.presentation_registry,
        auditor=auditor,
        name='Translation presentation exercise use case strategy',
    )

    regular_translation_test = Factory(
        ExerciseUseCaseStrategy,
        prefix='regular_translation_test',
        storage=user_command_storage,
        config_resolver=lang_config.translation_test_resolver,
        spec_factory_registry=spec_factories.test_registry,
        service_registry=services.regular_translation_test_registry,
        builder_registry=use_case_result_builders.test_registry,
        auditor=auditor,
        name='Translation test exercise use case strategy',
    )
