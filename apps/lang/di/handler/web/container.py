"""Language discipline web request handler DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Dict,
    Factory,
)

from apps.core.adapters.response import (
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
from apps.core.validators.request.null import NullValidator
from apps.lang.factories.lockup_factory import UserTranslationLookupFactory
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.translation.fetch import TranslationListRepository
from contracts.enums.exercise import ExerciseStatus


class WebHandlerContainer(DeclarativeContainer):
    """Language discipline web request handler DI container."""

    # =============================================
    # External dependencies
    # =============================================

    use_cases = DependenciesContainer()
    validators = DependenciesContainer()
    response_adapters = DependenciesContainer()

    user_command_storage = Dependency()  # type: ignore
    auditor = Dependency()  # type: ignore

    # =============================================
    # Translation presentation exercise strategy
    # =============================================

    regular_translation_presentation = Factory(
        RequestHandler,
        validator=validators.exercise_request,
        assembler=Factory(UserDataAssembler),
        use_case=use_cases.regular_translation_presentation,
        adapter=response_adapters.presentation_strategy,
        name='Regular translation presentation',
        auditor=auditor,
    )

    # =============================================
    # Translation test exercise strategy
    # =============================================

    web_test_exercise_adapter_registry = Dict(
        {
            ExerciseStatus.NEW_TASK: Factory(
                WebTestExerciseAdapter,
                templates=[],
            ),
            ExerciseStatus.EXPLAIN: Factory(
                WebExplainAdapter,
                extra_templates=[],
            ),
        }
    )
    process_regular_translation_test = Factory(
        RequestHandler,
        validator=validators.exercise_request,
        assembler=Factory(UserDataAssembler),
        use_case=use_cases.process_regular_translation_test,
        adapter=Factory(
            ProcessExerciseAdapterStrategy,
            registry=web_test_exercise_adapter_registry,
            auditor=auditor,
        ),
        name='Regular translation test',
        auditor=auditor,
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
