"""Mathematical discipline DI container."""

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Container, Dependency

from .adapter.web.exercise import ExerciseWebAdapterContainer
from .handler.web.exercise import ExerciseWebHandlerContainer
from .milestone.exercise import MilestoneContainer
from .repository.exercise import ExerciseRepositoryContainer
from .service.container import ExerciseServiceContainer
from .use_case.container import ExerciseUseCaseContainer
from .validator.web.exercise import ExerciseWebValidatorContainer
from .view.api.exercise import ApiViewContainer
from .view.web.container import WebViewContainer


class MathematicalContainer(DeclarativeContainer):
    """Mathematical discipline DI container."""

    # ===========================================
    # External dependencies
    # -------------------------------------------

    # Stores data by user ID, prefix, and optional kwargs
    user_data_storage = Dependency()  # type: ignore[var-annotated]
    reward_service = Dependency()  # type: ignore[var-annotated]

    # ===========================================
    # Internal dependencies
    # -------------------------------------------
    repositories = Container(
        ExerciseRepositoryContainer,
        cache_storage=user_data_storage,
    )
    exercise_services = Container(
        ExerciseServiceContainer,
    )
    milestone_services = Container(
        MilestoneContainer,
        reward_service=reward_service,
    )

    # ===========================================
    # View handler dependencies
    # -------------------------------------------
    web_validators = Container(
        ExerciseWebValidatorContainer,
    )
    use_cases = Container(
        ExerciseUseCaseContainer,
        storage=user_data_storage,
        repositories=repositories,
        exercise_services=exercise_services,
        milestone_services=milestone_services,
    )
    web_adapters = Container(
        ExerciseWebAdapterContainer,
    )

    # ===========================================
    # View handlers
    # -------------------------------------------
    web_handlers = Container(
        ExerciseWebHandlerContainer,
        validators=web_validators,
        use_cases=use_cases,
        adapters=web_adapters,
    )

    # ===========================================
    # Persistent references to the view handler
    # -------------------------------------------
    web_view = Container(
        WebViewContainer,
        handlers=web_handlers,
    )
    api_view = Container(
        ApiViewContainer,
    )
