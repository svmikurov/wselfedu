"""Language discipline web request handler DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Factory,
)

from apps.core.adapters.response.exercise.presentation.web import (
    WebPresentationAdapter,
)
from apps.core.adapters.response.exercise.test.web import WebTestAdapter
from apps.core.adapters.response.null import NullResponseAdapter
from apps.core.assemblers.assembler import UserAssembler, UserDataAssembler
from apps.core.domains.exercise import PresentationDomain
from apps.core.domains.exercise.enums import ExerciseTypeEnum
from apps.core.domains.exercise.selector import CandidatesSelector
from apps.core.handlers.generic import RequestHandler
from apps.core.services.exercise.generic import CreateExerciseService
from apps.core.use_cases.exercise.config_resolver import (
    ExerciseConfigurationResolver,
)
from apps.core.use_cases.exercise.generic import (
    ProcessExerciseUseCase,
    StartExerciseUseCase,
)
from apps.core.use_cases.repository import RepositoryUseCase
from apps.core.validators.request.null import NullValidator
from apps.core.validators.request.test import TestExerciseWebValidator
from apps.lang import models
from apps.lang.factories.dto_factory import PresentationDTOFactory
from apps.lang.factories.lockup_factory import UserTranslationLookupFactory
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.exercise.candidates.translation import (
    TranslationCandidatesRepository,
)
from apps.lang.repositories.legacy.exercise.conditions import (
    RegularParametersRepository,
)
from apps.lang.repositories.translation.fetch import TranslationListRepository


class WebHandlerContainer(DeclarativeContainer):
    """Language discipline web request handler DI container."""

    # =============================================
    # External dependencies
    # ---------------------------------------------
    use_cases = DependenciesContainer()

    user_command_storage = Dependency()

    # =============================================
    # Regular translation presentation
    # ---------------------------------------------
    start_regular_translation_presentation = Factory(
        RequestHandler,
        validator=Factory(NullValidator),
        assembler=Factory(UserAssembler),
        use_case=Factory(
            StartExerciseUseCase,
            config_resolver=Factory(
                ExerciseConfigurationResolver,
                exercise_type=ExerciseTypeEnum.PRESENTATION,
                parameters_repository=Factory(
                    RegularParametersRepository,
                    parameters_manager=models.ExerciseConditions.objects,
                    settings_manager=models.TranslationSetting.objects,
                ),
                default=None,
            ),
            service=Factory(
                CreateExerciseService,
                candidates_repository=Factory(
                    TranslationCandidatesRepository,
                    manager=EnglishTranslation.objects,
                ),
                domain=Factory(
                    PresentationDomain,
                    selector=Factory(CandidatesSelector),
                ),
                storage=user_command_storage,
            ),
            store_prefix='regular_translation_presentation',
            storage=user_command_storage,
            dto_factory=Factory(PresentationDTOFactory),
        ),
        adapter=Factory(
            WebPresentationAdapter,
            template_names=['lang/exercise/presentation/_mark_bar.html'],
        ),
    )
    process_regular_translation_presentation = Factory(
        RequestHandler,
        validator=...,
        assembler=Factory(UserDataAssembler),
        use_case=ProcessExerciseUseCase(
            strategy=...,
        ),
        adapter=...,
    )
    # =============================================
    # Regular translation test
    # ---------------------------------------------
    # Start translation test
    start_regular_translation_test = Factory(
        RequestHandler,
        validator=Factory(NullValidator),
        assembler=Factory(UserAssembler),
        use_case=use_cases.start_regular_translation_test,
        adapter=Factory(WebTestAdapter),
    )
    # ---------------------------------------------
    # Check user's answer on translation test
    # HACK: Update on check answer dependencies
    solve_regular_translation_test = Factory(
        RequestHandler,
        validator=Factory(TestExerciseWebValidator),
        assembler=Factory(UserDataAssembler),
        use_case=use_cases.solve_regular_translation_test,
        adapter=Factory(WebTestAdapter),
    )
    # =============================================
    # Translations
    # ---------------------------------------------
    english_translation_list = Factory(
        RequestHandler,
        validator=Factory(NullValidator),
        assembler=Factory(UserAssembler),
        use_case=Factory(
            RepositoryUseCase,
            lockup_factory=Factory(UserTranslationLookupFactory),
            repository=Factory(
                TranslationListRepository,
                manager=EnglishTranslation.objects,
            ),
        ),
        adapter=Factory(NullResponseAdapter),
    )
