"""Language discipline web request handler DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    DependenciesContainer,
    Dependency,
    Factory,
)

from apps.core.assemblers.assembler import UserAssembler, UserQueryAssembler
from apps.core.handlers.generic import RequestHandler
from apps.core.parsers.null import NullParser
from apps.core.use_cases.exercise.resource import (
    ExerciseCreateUseCase,
)
from apps.core.validators.request.null import NullValidator


class WebHandlerContainer(DeclarativeContainer):
    """Language discipline web request handler DI container."""

    # =============================================
    # External dependencies
    # ---------------------------------------------
    use_cases = DependenciesContainer()
    adapters = DependenciesContainer()

    storage = Dependency()

    # =============================================
    # Regular translation presentation
    # ---------------------------------------------
    start_regular_translation_presentation = Factory(
        RequestHandler,
        validator=Factory(NullValidator),
        assembler=Factory(UserAssembler),
        use_case=Factory(
            ExerciseCreateUseCase,
            repository=...,
            service=...,
            store_prefix='regular_translation_presentation',
            storage=storage,
            dto_factory=...,
        ),
        adapter=...,
    )

    # =============================================
    # Regular translation test exercise
    # ---------------------------------------------
    start_regular_translation_test = Factory(
        RequestHandler,
        validator=Factory(NullValidator),
        assembler=Factory(UserQueryAssembler, parser=Factory(NullParser)),
        use_case=...,
        adapter=...,
    )
