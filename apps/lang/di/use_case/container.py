"""Language discipline use case DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Factory,
)

from apps.core.domains.exercise import (
    TestExerciseCheckDomain,
    TestExerciseCreateDomain,
)
from apps.core.domains.exercise.dto import (
    ExerciseParametersDTO,
)
from apps.core.domains.exercise.enums import ExerciseTypeEnum
from apps.core.domains.exercise.selector import CandidatesSelector
from apps.core.domains.exercise.test.dto import TestExerciseConfigDTO
from apps.core.services.exercise.generic import (
    CheckExerciseService,
    CreateExerciseService,
    ExplainExerciseService,
)
from apps.core.use_cases.exercise.config_resolver import (
    ExerciseConfigurationResolver,
)
from apps.core.use_cases.exercise.generic import (
    CheckExerciseUseCase,
    StartExerciseUseCase,
)
from apps.lang import models
from apps.lang.factories.dto_factory import (
    TestExerciseDTOFactory,
)
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.exercise.candidates.translation import (
    TranslationCandidatesRepository,
)
from apps.lang.repositories.legacy.exercise.conditions import (
    RegularParametersRepository,
)


class UseCaseContainer(DeclarativeContainer):
    """Language discipline use case DI container."""

    # =============================================
    # External dependencies
    # ---------------------------------------------
    user_command_storage = Dependency()  # type: ignore[var-annotated]

    exercise_services = DependenciesContainer()
    milestone_services = DependenciesContainer()

    # =============================================
    # Regular translation test
    # ---------------------------------------------
    # Regular translation test dependencies
    # ---------------------------------------------
    regular_translation_test_config_resolver = Factory(
        ExerciseConfigurationResolver,
        exercise_type=ExerciseTypeEnum.TEST,
        parameters_repository=Factory(
            RegularParametersRepository,
            parameters_manager=models.ExerciseConditions.objects,
            settings_manager=models.TranslationSetting.objects,
        ),
        default=ExerciseParametersDTO(
            conf=TestExerciseConfigDTO(
                option_count=7,
            ),
        ),
    )
    # ---------------------------------------------
    # Start translation test
    # ---------------------------------------------
    start_regular_translation_test = Factory(
        StartExerciseUseCase,
        config_resolver=regular_translation_test_config_resolver,
        service=Factory(
            CreateExerciseService,
            candidates_repository=Factory(
                TranslationCandidatesRepository,
                manager=EnglishTranslation.objects,
            ),
            domain=Factory(
                TestExerciseCreateDomain,
                selector=Factory(CandidatesSelector),
            ),
            storage=user_command_storage,
        ),
        store_prefix='regular_translation_test',
        storage=user_command_storage,
        dto_factory=Factory(TestExerciseDTOFactory),
    )
    # ---------------------------------------------
    # Solve translation test
    # ---------------------------------------------
    solve_regular_translation_test = Factory(
        CheckExerciseUseCase,
        store_prefix='regular_translation_test',
        storage=user_command_storage,
        check_service=Factory(
            CheckExerciseService,
            domain=Factory(
                TestExerciseCheckDomain,
            ),
        ),
        config_resolver=regular_translation_test_config_resolver,
        milestone_service=None,
        create_use_case=start_regular_translation_test,
        explain_service=Factory(ExplainExerciseService),
    )
