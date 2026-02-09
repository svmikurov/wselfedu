"""Service DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Factory,
)

from apps.core.service.exercise import (
    DetailExerciseLoop,
    DetailTestCreate,
    RegularExerciseLoop,
    RegularTestCheck,
    RegularTestCreate,
    TestExplain,
)
from apps.lang.use_cases import (
    PresentationService,
    ProgressService,
)


class ServiceContainer(DeclarativeContainer):
    """Service DI container."""

    exercise_config = Dependency()  # type: ignore[var-annotated]
    progress_config = Dependency()  # type: ignore[var-annotated]

    repositories = DependenciesContainer()
    domains = DependenciesContainer()
    use_cases = DependenciesContainer()

    case_storage = Dependency()  # type: ignore[var-annotated]

    # ===========================================
    # Presentation
    # ===========================================

    regular_translation_presentation = Factory(
        PresentationService,
        repository=repositories.regular_translation_condition,  # Regular
        domain=domains.presentation,
        storage=case_storage,
    )

    # ===========================================
    # Test exercise
    # ===========================================

    explain_test_service = Factory(
        TestExplain,
    )

    # ---------------------------------
    # Regular translation test exercise
    # ---------------------------------

    detail_create_translation_test = Factory(
        DetailTestCreate,
        candidates_repository=repositories.detail_translation_exercise,
        storage=case_storage,
        domain=domains.create_detail_test,
        config=exercise_config,
    )
    regular_create_translation_test = Factory(
        RegularTestCreate,
        parameters_repository=repositories.regular_parameters,
        candidates_repository=repositories.regular_translation_exercise,
        storage=case_storage,
        domain=domains.create_regular_test,
        config=exercise_config,
    )

    check_translation_test_service = Factory(
        RegularTestCheck,
        domain=domains.check_test,
    )

    detail_test_loop = Factory(
        DetailExerciseLoop,  # Detail
        storage=case_storage,
        check_service=check_translation_test_service,
        create_service=detail_create_translation_test,  # Detail
        explain_service=explain_test_service,
        milestone_service=None,  # Implement points adding
    )
    regular_test_loop = Factory(
        RegularExerciseLoop,  # Regular
        storage=case_storage,
        check_service=check_translation_test_service,
        create_service=regular_create_translation_test,  # Regular
        explain_service=explain_test_service,
        milestone_service=None,
    )

    # ===========================================
    # Progress
    # ===========================================

    regular_translation_progress = Factory(
        ProgressService,
        repository=repositories.regular_translation_progress,
        case_storage=case_storage,
        config=progress_config,
    )
