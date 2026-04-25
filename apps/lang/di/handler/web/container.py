"""Language discipline web request handler DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Dict,
    Factory,
)

from apps.core.adapters.response.exercise.presentation.web import (
    PresentationTaskWebAdapter,
)
from apps.core.adapters.response.exercise.strategy import (
    ProcessExerciseAdapterStrategy,
)
from apps.core.adapters.response.exercise.test.web import (
    WebExplainAdapter,
    WebTestExerciseAdapter,
)
from apps.core.adapters.response.null import NullResponseAdapter
from apps.core.assemblers.assembler import UserAssembler, UserDataAssembler
from apps.core.handlers.generic import RequestHandler
from apps.core.repositories.use_case import RepositoryUseCase
from apps.core.validators.request.exercise.create_task import (
    CreateExerciseTaskValidator,
)
from apps.core.validators.request.null import NullValidator
from apps.lang.factories.lockup_factory import UserTranslationLookupFactory
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.translation.fetch import TranslationListRepository
from interfaces.enums.exercise import ExerciseStatus


class WebHandlerContainer(DeclarativeContainer):
    """Language discipline web request handler DI container."""

    # =============================================
    # External dependencies
    # ---------------------------------------------
    use_cases = DependenciesContainer()

    user_command_storage = Dependency()  # type: ignore

    # =============================================
    # Regular translation presentation
    # =============================================
    # QUESTION: Is deprecated?
    regular_translation_presentation = Factory(
        RequestHandler,
        validator=Factory(NullValidator),
        assembler=Factory(UserAssembler),
        use_case=use_cases.regular_translation_presentation,
        adapter=Factory(
            PresentationTaskWebAdapter,
            extra_oob_templates=['lang/exercise/presentation/_mark_bar.html'],
        ),
    )

    # ---------------------------------------------
    # Start presentation exercise
    # ---------------------------------------------
    # QUESTION: Is deprecated?
    start_regular_translation_presentation = Factory(
        RequestHandler,
        validator=Factory(NullValidator),
        assembler=Factory(UserAssembler),
        use_case=use_cases.start_regular_translation_presentation,
        adapter=Factory(
            PresentationTaskWebAdapter,
            extra_oob_templates=['lang/exercise/presentation/_mark_bar.html'],
        ),
    )
    # ---------------------------------------------
    # Process presentation exercise strategy
    # ---------------------------------------------
    presentation_adapter_registries = Dict(
        {
            ExerciseStatus.NEW_TASK: Factory(
                PresentationTaskWebAdapter,
                extra_oob_templates=[],
            ),
        },
    )
    process_regular_translation_presentation = Factory(
        RequestHandler,
        validator=Factory(CreateExerciseTaskValidator),
        assembler=Factory(UserDataAssembler),
        use_case=use_cases.process_regular_translation_presentation,
        adapter=Factory(
            ProcessExerciseAdapterStrategy,
            registry=presentation_adapter_registries,
        ),
    )

    # =============================================
    # Regular translation test
    # =============================================

    # ---------------------------------------------
    # Process test exercise strategy
    # ---------------------------------------------
    # TEST: Implement for translation test exercise
    web_test_exercise_adapter_registry = Dict(
        {
            ExerciseStatus.NEW_TASK: Factory(
                WebTestExerciseAdapter,
                extra_oob_templates=[],
            ),
            ExerciseStatus.EXPLAIN: Factory(
                WebExplainAdapter,
                extra_oob_templates=[],
            ),
        }
    )
    process_regular_translation_test = Factory(
        RequestHandler,
        validator=Factory(CreateExerciseTaskValidator),
        assembler=Factory(UserDataAssembler),
        use_case=use_cases.process_regular_translation_test,
        adapter=Factory(
            ProcessExerciseAdapterStrategy,
            registry=web_test_exercise_adapter_registry,
        ),
    )

    # QUESTION: Is deprecated?
    start_regular_translation_test = Factory(
        RequestHandler,
        validator=Factory(NullValidator),
        assembler=Factory(UserAssembler),
        use_case=use_cases.start_regular_translation_test,
        adapter=Factory(
            PresentationTaskWebAdapter,
            extra_oob_templates=[],
        ),
    )

    # =============================================
    # Translations
    # =============================================
    # QUESTION: Is deprecated?
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
