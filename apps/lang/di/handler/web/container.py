"""Language discipline web request handler DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Factory,
)

from apps.core.assemblers.impl import UserAssembler, UserDataAssembler
from apps.core.handlers.generic import RequestHandler
from apps.core.repositories.use_case import RepositoryUseCase
from apps.core.validators.request.null import NullValidator
from apps.lang.factories.lockup_factory import UserTranslationLookupFactory
from apps.lang.models import EnglishTranslation
from apps.lang.repositories.translation.fetch import TranslationListRepository
from kernel.adapter.null import NullResponseAdapter


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

    regular_translation_test = Factory(
        RequestHandler,
        validator=validators.exercise_request,
        assembler=Factory(UserDataAssembler),
        use_case=use_cases.regular_translation_test,
        adapter=response_adapters.test_strategy,
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
